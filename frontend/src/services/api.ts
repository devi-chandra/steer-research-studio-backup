import { Project, DashboardMetrics, HealthStatus, SettingsData, Claim, ContentDraft, Artifact } from '../types';

const getApiBase = (): string => {
  if (typeof window !== 'undefined') {
    if (window.location.port === '5173') return '';
    return `http://${window.location.hostname || '127.0.0.1'}:8000`;
  }
  return 'http://127.0.0.1:8000';
};

const API_BASE = getApiBase();

export const api = {
  // System & Health
  async getHealth(): Promise<HealthStatus> {
    const res = await fetch(`${API_BASE}/api/health`);
    if (!res.ok) throw new Error('Failed to fetch system health');
    return res.json();
  },

  async getDashboard(): Promise<DashboardMetrics> {
    const res = await fetch(`${API_BASE}/api/dashboard`);
    if (!res.ok) throw new Error('Failed to fetch dashboard metrics');
    return res.json();
  },

  async getSettings(): Promise<SettingsData> {
    const res = await fetch(`${API_BASE}/api/settings`);
    if (!res.ok) throw new Error('Failed to fetch settings');
    return res.json();
  },

  async updateSettings(data: Partial<SettingsData> & { gemini_api_key?: string; openai_api_key?: string }): Promise<SettingsData> {
    const res = await fetch(`${API_BASE}/api/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update settings');
    return res.json();
  },

  // Projects
  async listProjects(): Promise<Project[]> {
    const res = await fetch(`${API_BASE}/api/projects`);
    if (!res.ok) throw new Error('Failed to list projects');
    return res.json();
  },

  async getProject(projectId: string): Promise<Project> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}`);
    if (!res.ok) throw new Error('Failed to fetch project details');
    return res.json();
  },

  async createProject(data: { title: string; campaign_topic?: string; source_type: 'pdf' | 'url'; source_url?: string }): Promise<Project> {
    const res = await fetch(`${API_BASE}/api/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create project');
    return res.json();
  },

  async uploadPdf(projectId: string, file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(err.detail || 'Upload failed');
    }
    return res.json();
  },

  async processPipeline(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/process`, {
      method: 'POST',
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Pipeline processing failed' }));
      throw new Error(err.detail || 'Pipeline processing failed');
    }
    return res.json();
  },

  async deleteProject(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete project');
    return res.json();
  },

  // Claims & Medical Review Gate
  async getProjectClaims(projectId: string): Promise<Claim[]> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/claims`);
    if (!res.ok) throw new Error('Failed to fetch claims');
    return res.json();
  },

  async updateClaim(projectId: string, claimId: string, claimText: string, notes?: string): Promise<Claim> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/claims/${claimId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ claim_text: claimText, reviewer_notes: notes }),
    });
    if (!res.ok) throw new Error('Failed to update claim');
    return res.json();
  },

  async reviewClaim(
    projectId: string,
    claimId: string,
    action: 'approve' | 'reject' | 'flag' | 'edit',
    notes?: string,
    reviewerRole: string = 'Medical Reviewer',
    editedClaimText?: string
  ): Promise<Claim> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/claims/${claimId}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action,
        notes,
        reviewer_role: reviewerRole,
        edited_claim_text: editedClaimText,
      }),
    });
    if (!res.ok) throw new Error('Failed to record review action');
    return res.json();
  },

  // Draft & Media Generation
  async getDraft(projectId: string): Promise<ContentDraft> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/draft`);
    if (!res.ok) throw new Error('Failed to fetch content draft');
    return res.json();
  },

  async updateDraft(projectId: string, payload: Partial<ContentDraft>): Promise<ContentDraft> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/draft`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to update draft');
    return res.json();
  },

  async generateCarousel(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/generate-carousel`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to render carousel');
    return res.json();
  },

  async generateStatic(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/generate-static`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to render static post');
    return res.json();
  },

  async generateReel(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/generate-reel`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to render video reel');
    return res.json();
  },

  async getReelVoices(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/reel-voices`);
    if (!res.ok) throw new Error('Failed to fetch reel voices');
    return res.json();
  },

  async updateReelConfig(
    projectId: string,
    config: { mode: string; visual_style: string; language: string; voice_name?: string; visual_theme?: string }
  ): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/update-reel-config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    if (!res.ok) {
      let errDetail = 'Failed to update reel configuration';
      try {
        const errJson = await res.json();
        errDetail = errJson.detail || errJson.message || errDetail;
      } catch {
        const errText = await res.text().catch(() => '');
        if (errText) errDetail = errText;
      }
      throw new Error(errDetail);
    }
    return res.json();
  },

  async regenerateScene(
    projectId: string,
    sceneNumber: number,
    payload?: {
      narration?: string;
      subtitle_text?: string;
      on_screen_text?: string;
      visual_cue?: string;
      visual_style?: string;
      visual_theme?: string;
      animation_action?: string;
    }
  ): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/regenerate-scene/${sceneNumber}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload || {}),
    });
    if (!res.ok) throw new Error(`Failed to regenerate scene ${sceneNumber}`);
    return res.json();
  },

  getReelSceneThumbnailUrl(projectId: string, sceneNumber: number): string {
    return `${API_BASE}/api/projects/${projectId}/reel/scenes/${sceneNumber}/thumbnail`;
  },

  getReelSceneVideoUrl(projectId: string, sceneNumber: number): string {
    return `${API_BASE}/api/projects/${projectId}/reel/scenes/${sceneNumber}/video`;
  },

  async getReelManifest(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/reel/manifest`);
    if (!res.ok) throw new Error('Failed to fetch reel manifest');
    return res.json();
  },

  async getCrossFormatChecks(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/cross-format-checks`);
    if (!res.ok) throw new Error('Failed to fetch cross-format claim checks');
    return res.json();
  },

  // Artifacts & Exports
  async listArtifacts(projectId: string): Promise<Artifact[]> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/artifacts`);
    if (!res.ok) throw new Error('Failed to list artifacts');
    return res.json();
  },

  getArtifactFileUrl(artifactId: string, download: boolean = false): string {
    return `${API_BASE}/api/artifacts/${artifactId}/file${download ? '?download=true' : ''}`;
  },

  async buildAllExports(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/export/build-all`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to build exports');
    return res.json();
  },

  getPowerPointDownloadUrl(projectId: string): string {
    return `${API_BASE}/api/projects/${projectId}/export/powerpoint`;
  },

  async generatePowerPoint(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/export/powerpoint`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to generate PowerPoint presentation');
    return res.json();
  },

  async downloadPowerPointFile(projectId: string, defaultFilename?: string): Promise<void> {
    // 1. Force backend generation & artifact registration
    await this.generatePowerPoint(projectId);

    // 2. Fetch the .pptx file as a blob
    const downloadUrl = this.getPowerPointDownloadUrl(projectId);
    const res = await fetch(downloadUrl);
    if (!res.ok) {
      throw new Error(`Failed to download presentation (Status ${res.status})`);
    }

    const blob = await res.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = defaultFilename || `Steer_Presentation_${projectId.slice(0, 8)}.pptx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);
  },

  async updateEffort(projectId: string, manualEditSec?: number, manualReviewSec?: number): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/effort`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        manual_edit_seconds: manualEditSec,
        manual_review_seconds: manualReviewSec,
      }),
    });
    if (!res.ok) throw new Error('Failed to update effort tracking');
    return res.json();
  },
};

