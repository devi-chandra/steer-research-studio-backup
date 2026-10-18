export interface PaperMetadata {
  title?: string;
  authors?: string[];
  year?: number;
  doi?: string;
  journal?: string;
  abstract?: string;
  study_type?: string;
  key_findings?: string[];
  limitations?: string[];
  page_count?: number;
  pages_analyzed?: number;
  sample_size?: string;
}

export interface Claim {
  id: string;
  project_id: string;
  claim_id: string;
  claim_text: string;
  original_claim_text?: string;
  evidence_quote: string;
  source_document?: string;
  page_number?: number;
  section?: string;
  evidence_type: string;
  population?: string;
  sample_size?: string;
  limitations: string[];
  uncertainty_notes: string[];
  confidence_estimate?: number;
  verification_status: 'pending' | 'approved' | 'flagged' | 'rejected' | 'edited';
  support_level: 'strong' | 'moderate' | 'weak' | 'unsupported';
  support_notes?: string;
  reviewer_notes?: string;
  reviewed_by?: string;
  reviewed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface CarouselSlide {
  slide_number: number;
  eyebrow?: string;
  headline: string;
  body_text: string;
  key_stat?: string;
  stat_label?: string;
  practical_tip?: string;
  source_citation?: string;
  claim_ids: string[];
}

export interface StaticData {
  eyebrow?: string;
  headline: string;
  body_copy: string;
  practical_takeaway: string;
  badge?: string;
  source_citation?: string;
  claim_ids: string[];
}

export interface ReelScene {
  scene_number: number;
  duration_seconds: number;
  visual_cue: string;
  on_screen_text: string;
  narration: string;
  subtitle_text: string;
  visual_style?: string;
  visual_theme?: string;
  animation_action?: string;
  character_name?: string;
  organ_character?: string;
  claim_ids: string[];
  thumbnail_url?: string;
  video_url?: string;
  render_status?: 'ready' | 'rendering' | 'completed' | 'failed' | string;
  time_range?: string;
  start_time_seconds?: number;
  end_time_seconds?: number;
}

export interface ReelData {
  reel_title: string;
  hook: string;
  target_duration_seconds: number;
  practical_takeaway: string;
  mode?: 'everyday' | 'professional';
  visual_style?: string;
  visual_theme?: string;
  language?: string;
  voice_name?: string;
  scenes: ReelScene[];
  manifest?: any;
}

export interface ContentDraft {
  id: string;
  project_id: string;
  content_type: string;
  audience?: string;
  main_message?: string;
  hook?: string;
  body_copy?: string;
  practical_takeaway?: string;
  caption?: string;
  hashtags: string[];
  reasoning: {
    hook_rationale?: string;
    audience_relevance?: string;
    metabolic_principle?: string;
  };
  claim_ids: string[];
  slide_data?: CarouselSlide[];
  static_data?: StaticData;
  reel_data?: ReelData;
  created_at: string;
  updated_at: string;
}

export interface Artifact {
  id: string;
  project_id: string;
  artifact_type: 'carousel_slide' | 'carousel_zip' | 'static_post' | 'reel_video' | 'reel_audio' | 'captions_txt' | 'claims_export_json' | 'claims_export_csv' | 'project_summary' | 'powerpoint_pptx';
  filename: string;
  file_path: string;
  mime_type: string;

  file_size_bytes: number;
  metadata_json: Record<string, any>;
  created_at: string;
}

export interface EffortRecord {
  ingest_duration_ms: number;
  ai_extraction_duration_ms: number;
  ai_content_duration_ms: number;
  media_rendering_duration_ms: number;
  total_ai_duration_ms: number;
  manual_edit_seconds: number;
  manual_review_seconds: number;
  estimated_traditional_hours: number;
  estimated_time_saved_hours: number;
}

export interface Project {
  id: string;
  title: string;
  campaign_topic?: string;
  source_type: 'pdf' | 'url';
  source_filename?: string;
  source_url?: string;
  status: 'created' | 'ingesting' | 'extracting' | 'verifying' | 'translating' | 'content_ready' | 'reviewing' | 'approved' | 'completed' | 'error';
  current_stage: number;
  stage_message: string;
  error_message?: string;
  paper_metadata?: PaperMetadata;
  created_at: string;
  updated_at: string;
  claims: Claim[];
  content_drafts: ContentDraft[];
  artifacts: Artifact[];
  effort_record?: EffortRecord;
}

export interface DashboardMetrics {
  total_projects: number;
  total_claims: number;
  approved_claims: number;
  pending_claims: number;
  flagged_claims: number;
  rejected_claims: number;
  total_artifacts: number;
  total_hours_saved: number;
  recent_projects: Project[];
}

export interface HealthStatus {
  status: string;
  version: string;
  ai_provider: string;
  tts_engine: string;
  ffmpeg_available: boolean;
  database_connected: boolean;
}

export interface SettingsData {
  ai_provider: string;
  gemini_key_configured: boolean;
  openai_key_configured: boolean;
  tts_engine: string;
  tts_voice: string;
  storage_dir: string;
}
