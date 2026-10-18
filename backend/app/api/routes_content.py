import time
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.core.config import settings
from app.core.database import get_db
from app.models.models import Project, ContentDraft, Artifact
from app.services.carousel_renderer import carousel_renderer
from app.services.static_post_renderer import static_post_renderer
from app.services.video_generation import video_generation_service
from app.services.media_assembly import media_assembly_service
from app.services.effort_tracking import effort_tracking_service
from app.services.ai_provider import ai_provider_service
from app.schemas.schemas import ReelGenerateRequest, ReelSceneUpdateRequest

router = APIRouter(prefix="/api/projects/{project_id}", tags=["content"])

@router.get("/draft")
def get_draft(project_id: str, db: Session = Depends(get_db)):
    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="No content draft found for this project.")
    return draft

@router.put("/draft")
def update_draft(project_id: str, payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="No content draft found for this project.")

    for field in ["audience", "main_message", "hook", "caption", "hashtags", "slide_data", "static_data", "reel_data"]:
        if field in payload:
            setattr(draft, field, payload[field])

    db.commit()
    db.refresh(draft)
    return draft

@router.post("/generate-carousel")
@router.post("/generate/carousel")
def generate_carousel(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    if not draft or not draft.slide_data:
        raise HTTPException(status_code=400, detail="No carousel slide data available to render.")

    t_start = time.time()
    proj_gen_dir = settings.generated_dir / project_id
    proj_gen_dir.mkdir(parents=True, exist_ok=True)

    result = carousel_renderer.render_carousel_deck(
        slides=draft.slide_data,
        project_dir=proj_gen_dir
    )

    t_render_ms = int((time.time() - t_start) * 1000)

    # Remove old carousel artifacts
    db.query(Artifact).filter(
        Artifact.project_id == project_id,
        Artifact.artifact_type.in_(["carousel_slide", "carousel_zip"])
    ).delete()

    # Register individual slides
    for s_file in result["slide_files"]:
        p = Path(s_file)
        art = Artifact(
            project_id=project_id,
            artifact_type="carousel_slide",
            filename=p.name,
            file_path=str(p),
            mime_type="image/png",
            file_size_bytes=p.stat().st_size,
            metadata_json={"slide_number": int(p.stem.split("_")[-1])}
        )
        db.add(art)

    # Register ZIP bundle
    zip_p = Path(result["zip_file"])
    zip_art = Artifact(
        project_id=project_id,
        artifact_type="carousel_zip",
        filename=zip_p.name,
        file_path=str(zip_p),
        mime_type="application/zip",
        file_size_bytes=zip_p.stat().st_size,
        metadata_json={"slide_count": result["slide_count"]}
    )
    db.add(zip_art)

    # Track effort
    effort_tracking_service.record_automated_durations(db=db, project_id=project_id, rendering_ms=t_render_ms)

    project.stage_message = f"Rendered {result['slide_count']} carousel slides (1080x1350 PNG) and ZIP bundle."
    db.commit()

    return {
        "status": "success",
        "slide_count": result["slide_count"],
        "zip_file": zip_p.name,
        "rendering_time_ms": t_render_ms
    }

@router.post("/generate-static")
@router.post("/generate/static")
def generate_static_post(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    if not draft or not draft.static_data:
        raise HTTPException(status_code=400, detail="No static post data available to render.")

    t_start = time.time()
    proj_gen_dir = settings.generated_dir / project_id
    proj_gen_dir.mkdir(parents=True, exist_ok=True)

    out_file = proj_gen_dir / "static_post.png"
    static_post_renderer.render_static_post(post_data=draft.static_data, output_path=out_file)
    t_render_ms = int((time.time() - t_start) * 1000)

    # Register artifact
    db.query(Artifact).filter(
        Artifact.project_id == project_id,
        Artifact.artifact_type == "static_post"
    ).delete()

    art = Artifact(
        project_id=project_id,
        artifact_type="static_post",
        filename=out_file.name,
        file_path=str(out_file),
        mime_type="image/png",
        file_size_bytes=out_file.stat().st_size,
        metadata_json={"resolution": "1080x1350"}
    )
    db.add(art)

    effort_tracking_service.record_automated_durations(db=db, project_id=project_id, rendering_ms=t_render_ms)
    project.stage_message = "Rendered high-resolution Instagram static post (1080x1350 PNG)."
    db.commit()

    return {
        "status": "success",
        "filename": out_file.name,
        "file_size_bytes": out_file.stat().st_size,
        "rendering_time_ms": t_render_ms
    }

@router.get("/reel-voices")
def get_reel_voices(project_id: str):
    """Returns available Indian regional languages and compatible neural voices"""
    return ai_provider_service.get_available_voices()

VALID_THEMES = {"steer_brand", "warm_editorial", "colourful_cartoon", "playful_pastel", "pastel_educational", "cinematic", "clean_infographic", "inside_anatomy"}
VALID_STYLES = {"talking_characters", "characters", "inside_your_body", "everyday_human", "animated_explainer", "professional", "everyday"}

@router.post("/update-reel-config")
def update_reel_config(
    project_id: str,
    req: ReelGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Regenerates or translates the reel storyboard script to match the user's
    selected mode (everyday vs professional), visual style, visual theme, and regional language.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="No draft found")

    # Validate visual theme and style
    theme_to_use = req.visual_theme or "warm_editorial"
    if theme_to_use not in VALID_THEMES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported visual theme '{theme_to_use}'. Supported themes: {', '.join(sorted(VALID_THEMES))}"
        )

    if req.visual_style and req.visual_style not in VALID_STYLES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported visual style '{req.visual_style}'. Supported styles: 'talking_characters', 'inside_your_body', 'everyday_human', 'animated_explainer', 'professional'"
        )

    # Get claims for source grounding
    from app.models.models import Claim
    claims = db.query(Claim).filter(Claim.project_id == project_id).all()
    claims_list = [
        {"claim_id": c.claim_id, "claim_text": c.claim_text, "limitations": c.limitations}
        for c in claims
    ]

    new_reel_data = ai_provider_service.generate_regional_reel_script(
        mode=req.mode,
        visual_style=req.visual_style,
        visual_theme=theme_to_use,
        language=req.language,
        voice_name=req.voice_name,
        paper_title=project.title,
        claims=claims_list
    )

    draft.reel_data = new_reel_data
    db.commit()
    db.refresh(draft)

    return {
        "status": "success",
        "reel_data": new_reel_data
    }


@router.post("/regenerate-scene/{scene_number}")
async def regenerate_scene(
    project_id: str,
    scene_number: int,
    req: Optional[ReelSceneUpdateRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Regenerates a single scene's visual cue, narration, or re-renders its video
    without regenerating or invalidating the rest of the research project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    if not draft or not draft.reel_data:
        raise HTTPException(status_code=400, detail="No reel data available.")

    scenes = draft.reel_data.get("scenes", [])
    target_idx = None
    for idx, s in enumerate(scenes):
        if s.get("scene_number") == scene_number:
            target_idx = idx
            break

    if target_idx is None:
        raise HTTPException(status_code=404, detail=f"Scene {scene_number} not found.")

    current_scene = scenes[target_idx]
    mode = draft.reel_data.get("mode", "everyday")
    v_style = req.visual_style if (req and req.visual_style) else draft.reel_data.get("visual_style", "talking_characters")
    lang = draft.reel_data.get("language", "en")
    voice = draft.reel_data.get("voice_name")

    # If user provided direct edits to narration/subtitle
    if req:
        if req.narration:
            current_scene["narration"] = req.narration
        if req.subtitle_text:
            current_scene["subtitle_text"] = req.subtitle_text
        if req.on_screen_text:
            current_scene["on_screen_text"] = req.on_screen_text
        if req.visual_theme:
            if req.visual_theme not in VALID_THEMES:
                raise HTTPException(status_code=400, detail=f"Unsupported visual theme '{req.visual_theme}'.")
            current_scene["visual_theme"] = req.visual_theme
        if req.visual_style:
            if req.visual_style not in VALID_STYLES:
                raise HTTPException(status_code=400, detail=f"Unsupported visual style '{req.visual_style}'.")
            current_scene["visual_style"] = req.visual_style
            current_scene["animation_action"] = req.visual_style
        if req.animation_action:
            current_scene["animation_action"] = req.animation_action
    else:
        # Auto-regenerate fresh variation
        current_scene = ai_provider_service.regenerate_single_scene(
            scene_number=scene_number,
            mode=mode,
            visual_style=v_style,
            language=lang,
            current_scene=current_scene
        )

    scenes[target_idx] = current_scene
    draft.reel_data["scenes"] = scenes
    db.commit()

    # Re-render this single scene's animation and update final reel
    proj_gen_dir = settings.generated_dir / project_id / "reel"
    output_mp4 = proj_gen_dir / "final_reel.mp4"

    scene_render_res = await video_generation_service.render_animated_scene(
        scene=current_scene,
        scene_idx=target_idx,
        total_scenes=len(scenes),
        proj_reel_dir=proj_gen_dir,
        voice=voice,
        force_reencode=True
    )

    # Fast re-assembly of final reel using updated scene MP4
    if output_mp4.exists() or len(scenes) > 1:
        try:
            reel_res = await video_generation_service.render_full_animated_reel(
                scenes=scenes,
                proj_reel_dir=proj_gen_dir,
                output_mp4=output_mp4,
                voice=voice
            )
        except Exception as e:
            print(f"[Regen] Full reel re-concat failed: {e}")

    return {
        "status": "success",
        "scene_number": scene_number,
        "updated_scene": current_scene,
        "scene_render": scene_render_res
    }

@router.post("/generate-reel")
@router.post("/generate/reel")
async def generate_reel(project_id: str, db: Session = Depends(get_db)):
    """
    Renders actual vertical 9:16 MP4 video reel:
    1. Multi-frame procedural animation at 24fps (Talking characters, Inside Body, etc.)
    2. Synchronized regional neural voiceover & dynamic subtitle overlay
    3. H.264/AAC MP4 output verified for browser playback
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    draft = db.query(ContentDraft).filter(ContentDraft.project_id == project_id).first()
    if not draft or not draft.reel_data:
        raise HTTPException(status_code=400, detail="No reel data available to render.")

    t_start = time.time()
    proj_gen_dir = settings.generated_dir / project_id / "reel"
    proj_gen_dir.mkdir(parents=True, exist_ok=True)

    scenes = draft.reel_data.get("scenes", [])
    if not scenes:
        raise HTTPException(status_code=400, detail="Reel contains no scenes.")

    output_mp4 = proj_gen_dir / "final_reel.mp4"
    voice = draft.reel_data.get("voice_name") or settings.TTS_VOICE

    # Render all scenes and compile final animated reel
    reel_res = await video_generation_service.render_full_animated_reel(
        scenes=scenes,
        proj_reel_dir=proj_gen_dir,
        output_mp4=output_mp4,
        voice=voice
    )

    t_render_ms = int((time.time() - t_start) * 1000)

    # Clean old reel artifacts
    db.query(Artifact).filter(
        Artifact.project_id == project_id,
        Artifact.artifact_type.in_(["reel_video", "reel_scene_thumbnail", "reel_scene_video", "reel_manifest"])
    ).delete()

    # Register individual scene thumbnails and videos as artifacts
    for sc in scenes:
        s_num = sc.get("scene_number", 1)
        sc_dir = proj_gen_dir / f"scene_{s_num:02d}"
        thumb_f = sc_dir / "thumbnail.png"
        video_f = sc_dir / f"scene_{s_num:02d}.mp4"

        # Update accessible URLs and status
        sc["thumbnail_url"] = f"/api/projects/{project_id}/reel/scenes/{s_num}/thumbnail"
        sc["video_url"] = f"/api/projects/{project_id}/reel/scenes/{s_num}/video"
        sc["render_status"] = "completed"

        if thumb_f.exists():
            art_thumb = Artifact(
                project_id=project_id,
                artifact_type="reel_scene_thumbnail",
                filename=f"scene_{s_num:02d}_thumb.png",
                file_path=str(thumb_f),
                mime_type="image/png",
                file_size_bytes=thumb_f.stat().st_size,
                metadata_json={"scene_number": s_num}
            )
            db.add(art_thumb)

        if video_f.exists():
            art_sc_vid = Artifact(
                project_id=project_id,
                artifact_type="reel_scene_video",
                filename=f"scene_{s_num:02d}.mp4",
                file_path=str(video_f),
                mime_type="video/mp4",
                file_size_bytes=video_f.stat().st_size,
                metadata_json={"scene_number": s_num, "duration_seconds": sc.get("duration_seconds")}
            )
            db.add(art_sc_vid)

    # Register Manifest Artifact
    manifest_f = proj_gen_dir / "render_manifest.json"
    if manifest_f.exists():
        art_mf = Artifact(
            project_id=project_id,
            artifact_type="reel_manifest",
            filename="render_manifest.json",
            file_path=str(manifest_f),
            mime_type="application/json",
            file_size_bytes=manifest_f.stat().st_size,
            metadata_json={"scene_count": len(scenes), "total_duration_seconds": reel_res["duration_seconds"]}
        )
        db.add(art_mf)

    # Register Main Reel Video Artifact
    mp4_art = Artifact(
        project_id=project_id,
        artifact_type="reel_video",
        filename=output_mp4.name,
        file_path=str(output_mp4),
        mime_type="video/mp4",
        file_size_bytes=output_mp4.stat().st_size,
        metadata_json={
            "resolution": "1080x1920",
            "fps": 24,
            "duration_seconds": reel_res["duration_seconds"],
            "scenes_count": len(scenes),
            "mode": draft.reel_data.get("mode", "everyday"),
            "visual_style": draft.reel_data.get("visual_style", "talking_characters"),
            "language": draft.reel_data.get("language", "en"),
            "voice": voice,
            "pipeline": "procedural_24fps_animation"
        }
    )
    db.add(mp4_art)

    # Sync draft with updated manifest and actual scene durations
    draft.reel_data["scenes"] = scenes
    draft.reel_data["manifest"] = reel_res.get("manifest")
    draft.reel_data["target_duration_seconds"] = reel_res["duration_seconds"]
    db.commit()

    effort_tracking_service.record_automated_durations(db=db, project_id=project_id, rendering_ms=t_render_ms)
    project.stage_message = f"Rendered 24fps animated reel ({reel_res['duration_seconds']}s) in {draft.reel_data.get('language', 'en').upper()} with {len(scenes)} scenes."
    db.commit()

    return {
        "status": "success",
        "video_file": output_mp4.name,
        "file_size_bytes": output_mp4.stat().st_size,
        "rendering_time_ms": t_render_ms,
        "duration_seconds": reel_res["duration_seconds"],
        "pipeline": "procedural_24fps_animation",
        "mode": draft.reel_data.get("mode", "everyday"),
        "visual_style": draft.reel_data.get("visual_style", "talking_characters"),
        "language": draft.reel_data.get("language", "en"),
        "scenes": scenes,
        "manifest": reel_res.get("manifest")
    }

@router.get("/reel/scenes/{scene_number}/thumbnail")
def get_scene_thumbnail(project_id: str, scene_number: int):
    from fastapi.responses import FileResponse
    proj_gen_dir = settings.generated_dir / project_id / "reel"
    thumb_path = proj_gen_dir / f"scene_{scene_number:02d}" / "thumbnail.png"
    if not thumb_path.exists():
        raise HTTPException(status_code=404, detail=f"Thumbnail for scene {scene_number} not found.")
    return FileResponse(str(thumb_path), media_type="image/png")

@router.get("/reel/scenes/{scene_number}/video")
def get_scene_video(project_id: str, scene_number: int):
    from fastapi.responses import FileResponse
    proj_gen_dir = settings.generated_dir / project_id / "reel"
    video_path = proj_gen_dir / f"scene_{scene_number:02d}" / f"scene_{scene_number:02d}.mp4"
    if not video_path.exists():
        raise HTTPException(status_code=404, detail=f"Video for scene {scene_number} not found.")
    return FileResponse(str(video_path), media_type="video/mp4")

@router.get("/reel/manifest")
def get_reel_manifest(project_id: str):
    import json
    proj_gen_dir = settings.generated_dir / project_id / "reel"
    manifest_path = proj_gen_dir / "render_manifest.json"
    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="Render manifest not found. Render reel first.")
    with open(manifest_path, "r", encoding="utf-8") as mf:
        return json.load(mf)
