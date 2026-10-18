from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.models import Project, Claim, ContentDraft, Artifact, EffortRecord
from app.services.export_service import export_service
from app.services.effort_tracking import effort_tracking_service

router = APIRouter(prefix="/api/projects/{project_id}/export", tags=["export"])

@router.post("/build-all")
def build_all_exports(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    claims = db.query(Claim).filter(Claim.project_id == project_id).order_by(Claim.claim_id).all()
    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    effort = effort_tracking_service.get_or_create_effort_record(db, project_id)

    export_dir = settings.generated_dir / project_id / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    created_artifacts = []

    # 1. Captions TXT
    if draft:
        cap_file = export_dir / "captions_and_hashtags.txt"
        export_service.generate_captions_txt(draft, cap_file)
        db.query(Artifact).filter(Artifact.project_id == project_id, Artifact.artifact_type == "captions_txt").delete()
        cap_art = Artifact(
            project_id=project_id,
            artifact_type="captions_txt",
            filename=cap_file.name,
            file_path=str(cap_file),
            mime_type="text/plain",
            file_size_bytes=cap_file.stat().st_size
        )
        db.add(cap_art)
        created_artifacts.append(cap_art)

    # 2. Claims JSON
    if claims:
        json_file = export_dir / "claims_evidence_ledger.json"
        export_service.generate_claims_json(claims, project, json_file)
        db.query(Artifact).filter(Artifact.project_id == project_id, Artifact.artifact_type == "claims_export_json").delete()
        json_art = Artifact(
            project_id=project_id,
            artifact_type="claims_export_json",
            filename=json_file.name,
            file_path=str(json_file),
            mime_type="application/json",
            file_size_bytes=json_file.stat().st_size
        )
        db.add(json_art)
        created_artifacts.append(json_art)

        # 3. Claims CSV
        csv_file = export_dir / "claims_evidence_ledger.csv"
        export_service.generate_claims_csv(claims, csv_file)
        db.query(Artifact).filter(Artifact.project_id == project_id, Artifact.artifact_type == "claims_export_csv").delete()
        csv_art = Artifact(
            project_id=project_id,
            artifact_type="claims_export_csv",
            filename=csv_file.name,
            file_path=str(csv_file),
            mime_type="text/csv",
            file_size_bytes=csv_file.stat().st_size
        )
        db.add(csv_art)
        created_artifacts.append(csv_art)

    # 4. Project Summary
    sum_file = export_dir / "project_audit_summary.json"
    export_service.generate_project_summary(project, claims, effort, sum_file)
    db.query(Artifact).filter(Artifact.project_id == project_id, Artifact.artifact_type == "project_summary").delete()
    sum_art = Artifact(
        project_id=project_id,
        artifact_type="project_summary",
        filename=sum_file.name,
        file_path=str(sum_file),
        mime_type="application/json",
        file_size_bytes=sum_file.stat().st_size
    )
    db.add(sum_art)
    created_artifacts.append(sum_art)

    # 5. PowerPoint Presentation (.pptx)
    ppt_file = export_dir / f"steer_clinical_briefing_{project_id[:8]}.pptx"
    export_service.generate_powerpoint_presentation(project, claims, draft, ppt_file)
    db.query(Artifact).filter(Artifact.project_id == project_id, Artifact.artifact_type == "powerpoint_pptx").delete()
    ppt_art = Artifact(
        project_id=project_id,
        artifact_type="powerpoint_pptx",
        filename=ppt_file.name,
        file_path=str(ppt_file),
        mime_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        file_size_bytes=ppt_file.stat().st_size
    )
    db.add(ppt_art)
    created_artifacts.append(ppt_art)

    db.commit()

    return {
        "status": "success",
        "exported_count": len(created_artifacts),
        "message": "All export packages including PowerPoint generated successfully."
    }

@router.get("/powerpoint")
@router.get("/pptx")
def download_powerpoint(project_id: str, db: Session = Depends(get_db)):
    """
    Returns the PowerPoint (.pptx) file for the project, generating it on the fly if needed.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    export_dir = settings.generated_dir / project_id / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    ppt_file = export_dir / f"steer_clinical_briefing_{project_id[:8]}.pptx"

    if not ppt_file.exists():
        claims = db.query(Claim).filter(Claim.project_id == project_id).order_by(Claim.claim_id).all()
        draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
        export_service.generate_powerpoint_presentation(project, claims, draft, ppt_file)

        # Register artifact
        db.query(Artifact).filter(Artifact.project_id == project_id, Artifact.artifact_type == "powerpoint_pptx").delete()
        ppt_art = Artifact(
            project_id=project_id,
            artifact_type="powerpoint_pptx",
            filename=ppt_file.name,
            file_path=str(ppt_file),
            mime_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            file_size_bytes=ppt_file.stat().st_size
        )
        db.add(ppt_art)
        db.commit()

    safe_title = "".join(c for c in (project.title or "presentation") if c.isalnum() or c in ("-", "_")).rstrip()
    download_filename = f"Steer_Presentation_{safe_title[:30]}_{project_id[:6]}.pptx"

    return FileResponse(
        path=str(ppt_file),
        filename=download_filename,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

@router.post("/powerpoint")
def generate_powerpoint_endpoint(project_id: str, db: Session = Depends(get_db)):
    """
    Explicitly forces generation/regeneration of the PowerPoint presentation.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    claims = db.query(Claim).filter(Claim.project_id == project_id).order_by(Claim.claim_id).all()
    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    export_dir = settings.generated_dir / project_id / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    ppt_file = export_dir / f"steer_clinical_briefing_{project_id[:8]}.pptx"

    export_service.generate_powerpoint_presentation(project, claims, draft, ppt_file)

    db.query(Artifact).filter(Artifact.project_id == project_id, Artifact.artifact_type == "powerpoint_pptx").delete()
    ppt_art = Artifact(
        project_id=project_id,
        artifact_type="powerpoint_pptx",
        filename=ppt_file.name,
        file_path=str(ppt_file),
        mime_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        file_size_bytes=ppt_file.stat().st_size
    )
    db.add(ppt_art)
    db.commit()

    return {
        "status": "success",
        "filename": ppt_file.name,
        "size_bytes": ppt_file.stat().st_size,
        "download_url": f"/api/projects/{project_id}/export/powerpoint"
    }

