import os
import shutil
import time
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.config import settings
from app.core.database import get_db
from app.models.models import Project, Claim, ContentDraft, Artifact, EffortRecord
from app.schemas.schemas import ProjectCreate, ProjectResponse
from app.services.pdf_extraction import PDFExtractionService
from app.services.url_ingestion import URLIngestionService
from app.services.ai_provider import ai_provider_service
from app.services.evidence_tracking import EvidenceTrackingService
from app.services.effort_tracking import effort_tracking_service

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return projects

@router.post("", response_model=ProjectResponse)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(
        title=data.title.strip(),
        campaign_topic=data.campaign_topic.strip() if data.campaign_topic else None,
        source_type=data.source_type,
        source_url=data.source_url.strip() if data.source_url else None,
        status="created",
        current_stage=1,
        stage_message="Project created. Ready for paper ingestion."
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Initialize effort record
    effort_tracking_service.get_or_create_effort_record(db, project.id)

    return project

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/{project_id}/upload")
async def upload_pdf(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF scientific papers are accepted.")

    # Save to uploads dir under project folder
    proj_upload_dir = settings.uploads_dir / project_id
    proj_upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Safe filename
    clean_filename = "".join(c for c in file.filename if c.isalnum() or c in "._- ")
    target_path = proj_upload_dir / clean_filename

    contents = await file.read()
    if len(contents) > 50 * 1024 * 1024:  # 50MB limit
        raise HTTPException(status_code=400, detail="File too large. Maximum PDF size is 50MB.")
    if len(contents) < 500:
        raise HTTPException(status_code=400, detail="File too small or corrupted.")

    with open(target_path, "wb") as f:
        f.write(contents)

    project.source_filename = clean_filename
    project.source_type = "pdf"
    project.stage_message = f"Uploaded PDF: {clean_filename}. Ready to process."
    db.commit()
    db.refresh(project)

    return {
        "status": "success",
        "project_id": project_id,
        "filename": clean_filename,
        "size_bytes": len(contents)
    }

@router.post("/{project_id}/process")
async def process_project_pipeline(project_id: str, db: Session = Depends(get_db)):
    """
    Executes the automated stages:
    1. Ingestion (PDF / URL)
    2. Extraction of claims with exact quotes and metadata
    3. Verification of evidence against source paper
    4. Translation into Steer's brand voice
    5. Draft creation for Carousel, Static, and Reel
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    t_start = time.time()
    try:
        # Stage 1: Ingestion
        project.status = "ingesting"
        project.current_stage = 1
        project.stage_message = "Stage 1/7: Ingesting scientific paper and extracting text pages..."
        db.commit()

        extracted_data = None
        t_ingest_start = time.time()

        if project.source_type == "pdf":
            if not project.source_filename:
                # Check if sample paper exists or raise error
                sample_pdf = settings.sample_papers_dir / "sample_postprandial_walk_study.pdf"
                if sample_pdf.exists():
                    target_pdf = sample_pdf
                    project.source_filename = sample_pdf.name
                else:
                    raise HTTPException(status_code=400, detail="No PDF file uploaded for this project.")
            else:
                target_pdf = settings.uploads_dir / project_id / project.source_filename

            extracted_data = PDFExtractionService.extract_pdf(target_pdf)
        else:
            # URL ingestion
            if not project.source_url:
                raise HTTPException(status_code=400, detail="No source URL provided.")
            extracted_data = await URLIngestionService.fetch_paper_from_url(project.source_url)

        t_ingest_ms = int((time.time() - t_ingest_start) * 1000)

        # Update project title if extracted title is a real paper title
        ext_title = extracted_data.get("title")
        if ext_title and len(ext_title) > 5 and not ext_title.lower().endswith(".pdf"):
            project.title = ext_title

        # Stage 2: AI Claim Extraction
        project.status = "extracting"
        project.current_stage = 2
        project.stage_message = "Stage 2/7: Extracting structured claims, quantitative findings, and exact quotes..."
        project.paper_metadata = {
            "title": ext_title or project.title,
            "authors": extracted_data.get("authors") or [],
            "year": extracted_data.get("year"),
            "doi": extracted_data.get("doi"),
            "journal": extracted_data.get("journal"),
            "study_type": extracted_data.get("study_type"),
            "abstract": extracted_data.get("abstract"),
            "page_count": extracted_data.get("page_count"),
            "pages_analyzed": extracted_data.get("pages_analyzed", extracted_data.get("page_count"))
        }
        project.extracted_text_pages = extracted_data.get("pages")
        db.commit()

        t_extract_start = time.time()
        ai_extraction_result = await ai_provider_service.extract_claims_and_metadata(
            paper_text=extracted_data.get("full_text", ""),
            paper_metadata=project.paper_metadata,
            pages=extracted_data.get("pages", [])
        )
        t_extract_ms = int((time.time() - t_extract_start) * 1000)

        # Update metadata if AI found deeper info
        ai_meta = ai_extraction_result.get("metadata", {})
        if ai_meta:
            updated_meta = dict(project.paper_metadata)
            for k, v in ai_meta.items():
                if v:
                    updated_meta[k] = v
            project.paper_metadata = updated_meta
            if updated_meta.get("title") and len(updated_meta["title"]) > 5:
                project.title = updated_meta["title"]
        db.commit()


        # Stage 3: Evidence Verification Ledger
        project.status = "verifying"
        project.current_stage = 3
        project.stage_message = "Stage 3/7: Cross-examining quotes against source paper text..."
        db.commit()

        # Clear any prior claims on re-run
        db.query(Claim).filter(Claim.project_id == project_id).delete()

        claims_list = ai_extraction_result.get("claims", [])
        persisted_claims: List[Claim] = []

        for c_data in claims_list:
            # Cross-examine quote
            verif_result = EvidenceTrackingService.verify_claim_evidence(
                claim=c_data,
                full_paper_text=extracted_data.get("full_text", ""),
                pages=extracted_data.get("pages", [])
            )

            claim_obj = Claim(
                project_id=project_id,
                claim_id=c_data.get("claim_id", f"CLM-{len(persisted_claims)+1:03d}"),
                claim_text=c_data.get("claim_text", ""),
                evidence_quote=c_data.get("evidence_quote", ""),
                source_document=project.source_filename or project.source_url or "Scientific Paper",
                page_number=c_data.get("page_number"),
                section=c_data.get("section", "Results"),
                evidence_type=c_data.get("evidence_type", "Unknown"),
                population=c_data.get("population"),
                sample_size=c_data.get("sample_size"),
                limitations=c_data.get("limitations", []),
                uncertainty_notes=c_data.get("uncertainty_notes", []),
                confidence_estimate=verif_result.get("confidence_estimate"),
                verification_status=verif_result.get("verification_status", "pending"),
                support_level=verif_result.get("support_level", "strong"),
                support_notes=verif_result.get("support_notes")
            )
            db.add(claim_obj)
            persisted_claims.append(claim_obj)

        db.commit()

        # Stage 4 & 5: Steer Voice Translation & Content Drafting
        project.status = "translating"
        project.current_stage = 4
        project.stage_message = "Stage 4/7: Translating scientific findings into Steer's doctor-led voice..."
        db.commit()

        t_content_start = time.time()
        claims_for_prompt = [
            {
                "claim_id": c.claim_id,
                "claim_text": c.claim_text,
                "evidence_quote": c.evidence_quote,
                "limitations": c.limitations
            }
            for c in persisted_claims
        ]

        steer_content = await ai_provider_service.generate_steer_content(
            paper_title=project.paper_metadata.get("title", project.title),
            claims=claims_for_prompt,
            campaign_topic=project.campaign_topic
        )
        t_content_ms = int((time.time() - t_content_start) * 1000)

        # Clear prior drafts
        db.query(ContentDraft).filter(ContentDraft.project_id == project_id).delete()

        # Persist Master Draft
        draft = ContentDraft(
            project_id=project_id,
            content_type="master_campaign",
            audience=steer_content.get("audience"),
            main_message=steer_content.get("main_message"),
            hook=steer_content.get("hook"),
            caption=steer_content.get("caption"),
            hashtags=steer_content.get("hashtags", []),
            reasoning=steer_content.get("reasoning", {}),
            claim_ids=steer_content.get("claim_ids", [c.claim_id for c in persisted_claims]),
            slide_data=steer_content.get("carousel", {}).get("slides", []),
            static_data=steer_content.get("static_post", {}),
            reel_data=steer_content.get("reel", {})
        )
        db.add(draft)

        # Update project status
        project.status = "content_ready"
        project.current_stage = 5
        project.stage_message = "Content draft generated. Ready for media rendering and medical review."
        db.commit()

        # Track effort
        effort_tracking_service.record_automated_durations(
            db=db,
            project_id=project_id,
            ingest_ms=t_ingest_ms,
            extraction_ms=t_extract_ms,
            content_ms=t_content_ms
        )

        db.refresh(project)
        return {
            "status": "success",
            "project_id": project_id,
            "claims_count": len(persisted_claims),
            "stages_completed": 5,
            "message": "Scientific extraction, evidence cross-examination, and Steer drafting completed successfully."
        }

    except Exception as e:
        project.status = "error"
        project.error_message = str(e)
        project.stage_message = f"Error in pipeline: {str(e)}"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Clean up files on disk
    upload_path = settings.uploads_dir / project_id
    if upload_path.exists():
        shutil.rmtree(upload_path, ignore_errors=True)
        
    gen_path = settings.generated_dir / project_id
    if gen_path.exists():
        shutil.rmtree(gen_path, ignore_errors=True)

    db.delete(project)
    db.commit()
    return {"status": "success", "message": f"Project {project_id} deleted"}

@router.get("/{project_id}/cross-format-checks")
def get_project_cross_format_checks(project_id: str, db: Session = Depends(get_db)):
    from app.models.models import ContentDraft, Claim
    from app.services.cross_format_claims import cross_format_claims_service

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    claims = db.query(Claim).filter(Claim.project_id == project_id).all()

    return cross_format_claims_service.audit_project_consistency(project=project, draft=draft, claims=claims)
