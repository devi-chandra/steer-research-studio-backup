import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Layers, 
  ShieldCheck, 
  Download, 
  Clock, 
  ArrowLeft, 
  Sparkles, 
  RotateCw,
  Trash2,
  AlertTriangle
} from 'lucide-react';
import { Project, DashboardMetrics as MetricsType, HealthStatus, ContentDraft } from './types';
import { api } from './services/api';

import { Navbar } from './components/Navbar';
import { DashboardMetrics } from './components/DashboardMetrics';
import { NewProjectModal } from './components/NewProjectModal';
import { ProcessingProgress } from './components/ProcessingProgress';
import { ResearchLedger } from './components/ResearchLedger';
import { MedicalReviewDashboard } from './components/MedicalReviewDashboard';
import { ContentStudio } from './components/ContentStudio';
import { ExportCenter } from './components/ExportCenter';
import { EffortTrackerModal } from './components/EffortTrackerModal';
import { SettingsModal } from './components/SettingsModal';

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [metrics, setMetrics] = useState<MetricsType | null>(null);
  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);
  const [project, setProject] = useState<Project | null>(null);
  const [draft, setDraft] = useState<ContentDraft | null>(null);

  // Active view in project: 'evidence' | 'content' | 'review' | 'export'
  const [activeView, setActiveView] = useState<'evidence' | 'content' | 'review' | 'export'>('content');

  // Modals
  const [isNewProjectOpen, setIsNewProjectOpen] = useState<boolean>(false);
  const [isEffortOpen, setIsEffortOpen] = useState<boolean>(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState<boolean>(false);
  const [selectedClaimIdForReview, setSelectedClaimIdForReview] = useState<string | null>(null);
  const [isQuickStarting, setIsQuickStarting] = useState<boolean>(false);

  // Load health & metrics on mount
  useEffect(() => {
    loadHealthAndMetrics();
  }, []);

  // When activeProjectId changes, load project & draft
  useEffect(() => {
    if (activeProjectId) {
      loadProjectDetails(activeProjectId);
    } else {
      setProject(null);
      setDraft(null);
    }
  }, [activeProjectId]);

  const loadHealthAndMetrics = async () => {
    try {
      const [h, m] = await Promise.all([api.getHealth(), api.getDashboard()]);
      setHealth(h);
      setMetrics(m);
    } catch (err) {
      console.error('Initial load error:', err);
    }
  };

  const loadProjectDetails = async (id: string) => {
    try {
      const p = await api.getProject(id);
      setProject(p);
      try {
        const d = await api.getDraft(id);
        setDraft(d);
      } catch {
        setDraft(null);
      }
    } catch (err) {
      console.error('Failed to load project details:', err);
    }
  };

  const handleRefreshProject = () => {
    if (activeProjectId) {
      loadProjectDetails(activeProjectId);
    }
    loadHealthAndMetrics();
  };

  // Quick Start Sample Paper Demo
  const handleQuickStartDemo = async () => {
    setIsQuickStarting(true);
    try {
      // 1. Create Project
      const proj = await api.createProject({
        title: 'Postprandial Walking & Glycemic Excursions in South Asian Adults',
        campaign_topic: 'Shatapadi (100 Steps After Meals)',
        source_type: 'pdf',
      });

      // 2. Trigger pipeline processing (will automatically pick up the pre-built sample paper)
      await api.processPipeline(proj.id);

      setIsQuickStarting(false);
      setActiveProjectId(proj.id);
      setActiveView('content');
      loadHealthAndMetrics();
    } catch (err: any) {
      setIsQuickStarting(false);
      alert(`Quick start demo failed: ${err.message}`);
    }
  };

  const handleDeleteProject = async () => {
    if (!project) return;
    if (confirm(`Are you sure you want to delete "${project.title}"?`)) {
      try {
        await api.deleteProject(project.id);
        setActiveProjectId(null);
        loadHealthAndMetrics();
      } catch (err: any) {
        alert(`Delete failed: ${err.message}`);
      }
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <Navbar
        health={health}
        onOpenNewProject={() => setIsNewProjectOpen(true)}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onGoHome={() => setActiveProjectId(null)}
        activeProjectTitle={project?.title}
      />

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: '36px 0 60px' }}>
        <div className="steer-container">
          {!activeProjectId ? (
            /* Dashboard View */
            <DashboardMetrics
              metrics={metrics}
              onSelectProject={(id) => {
                setActiveProjectId(id);
                loadProjectDetails(id);
              }}
              onOpenNewProject={() => setIsNewProjectOpen(true)}
              onQuickStartDemo={handleQuickStartDemo}
              isQuickStarting={isQuickStarting}
            />
          ) : (
            /* Active Project Studio View */
            project && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
                {/* Project Header Bar */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: '16px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                    <button
                      onClick={() => setActiveProjectId(null)}
                      className="btn-secondary"
                      style={{ padding: '8px 14px', fontSize: '13px' }}
                    >
                      <ArrowLeft size={16} />
                      <span>Dashboard</span>
                    </button>
                    <div>
                      <div className="badge-tag badge-blush" style={{ marginBottom: '4px' }}>
                        ACTIVE RESEARCH PROJECT
                      </div>
                      <h1 style={{ fontSize: '26px', color: 'var(--color-ink)', lineHeight: 1.25 }}>
                        {project.title}
                      </h1>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <button
                      onClick={() => setIsEffortOpen(true)}
                      className="btn-secondary"
                      style={{ fontSize: '13px', padding: '8px 16px' }}
                    >
                      <Clock size={15} color="var(--color-rust)" />
                      <span>Effort: {project.effort_record?.estimated_time_saved_hours || 4.0}h Saved</span>
                    </button>

                    <button
                      onClick={handleRefreshProject}
                      className="btn-secondary"
                      style={{ padding: '8px 12px' }}
                      title="Refresh Project Data"
                    >
                      <RotateCw size={15} />
                    </button>

                    <button
                      onClick={handleDeleteProject}
                      className="btn-secondary"
                      style={{ padding: '8px 12px', color: '#C62828' }}
                      title="Delete Project"
                    >
                      <Trash2 size={15} />
                    </button>
                  </div>
                </div>

                {/* 7-Stage Pipeline Progress Bar */}
                <ProcessingProgress
                  project={project}
                  onRetry={() => api.processPipeline(project.id).then(handleRefreshProject)}
                />

                {/* Main Studio View Switcher Tabs */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  borderBottom: '2px solid var(--color-card-border)',
                  paddingBottom: '12px'
                }}>
                  <button
                    onClick={() => setActiveView('content')}
                    className={`steer-tab-btn ${activeView === 'content' ? 'active' : ''}`}
                    style={{ fontSize: '16px', padding: '12px 24px' }}
                  >
                    <Sparkles size={18} />
                    <span>Content Studio (Carousel • Static • Reel • PowerPoint)</span>
                  </button>

                  <button
                    onClick={() => setActiveView('evidence')}
                    className={`steer-tab-btn ${activeView === 'evidence' ? 'active' : ''}`}
                    style={{ fontSize: '16px', padding: '12px 24px' }}
                  >
                    <FileText size={18} />
                    <span>Research Details & Evidence Ledger</span>
                  </button>

                  <button
                    onClick={() => setActiveView('review')}
                    className={`steer-tab-btn ${activeView === 'review' ? 'active' : ''}`}
                    style={{ fontSize: '16px', padding: '12px 24px' }}
                  >
                    <ShieldCheck size={18} />
                    <span>Medical Review Gate</span>
                    {project.claims && project.claims.some((c) => c.verification_status === 'pending') && (
                      <span style={{
                        background: '#E65100',
                        color: '#FFFFFF',
                        borderRadius: '10px',
                        padding: '1px 7px',
                        fontSize: '11px',
                        fontWeight: 700
                      }}>
                        {project.claims.filter((c) => c.verification_status === 'pending').length}
                      </span>
                    )}
                  </button>

                  <button
                    onClick={() => setActiveView('export')}
                    className={`steer-tab-btn ${activeView === 'export' ? 'active' : ''}`}
                    style={{ fontSize: '16px', padding: '12px 24px' }}
                  >
                    <Download size={18} />
                    <span>Export Center</span>
                  </button>
                </div>

                {/* View Container */}
                <div>
                  {activeView === 'content' && (
                    <ContentStudio
                      project={project}
                      draft={draft}
                      onRefresh={handleRefreshProject}
                    />
                  )}

                  {activeView === 'evidence' && (
                    <ResearchLedger
                      project={project}
                      onOpenReview={(claimId) => {
                        setSelectedClaimIdForReview(claimId);
                        setActiveView('review');
                      }}
                      onOpenPassage={() => {
                        setActiveView('evidence');
                      }}
                    />
                  )}

                  {activeView === 'review' && (
                    <MedicalReviewDashboard
                      project={project}
                      onClaimUpdated={handleRefreshProject}
                      selectedClaimId={selectedClaimIdForReview}
                    />
                  )}

                  {activeView === 'export' && (
                    <ExportCenter
                      project={project}
                      onRefresh={handleRefreshProject}
                    />
                  )}
                </div>
              </div>
            )
          )}
        </div>
      </main>

      {/* Modals */}
      <NewProjectModal
        isOpen={isNewProjectOpen}
        onClose={() => setIsNewProjectOpen(false)}
        onProjectCreated={(id) => {
          setActiveProjectId(id);
          loadProjectDetails(id);
          setActiveView('content');
          loadHealthAndMetrics();
        }}
        onLoadSamplePaper={handleQuickStartDemo}
      />

      {project && (
        <EffortTrackerModal
          isOpen={isEffortOpen}
          onClose={() => setIsEffortOpen(false)}
          project={project}
          onUpdated={handleRefreshProject}
        />
      )}

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSettingsUpdated={loadHealthAndMetrics}
        health={health}
      />
    </div>
  );
};

export default App;
