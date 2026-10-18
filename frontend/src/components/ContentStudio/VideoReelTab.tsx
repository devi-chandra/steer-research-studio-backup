import React, { useState } from 'react';
import { 
  Play, 
  RotateCw, 
  Download, 
  Film, 
  Volume2, 
  Sparkles, 
  Clock, 
  Layers, 
  ShieldCheck, 
  CheckCircle2,
  Video,
  Languages,
  Activity,
  HeartPulse,
  UserCheck,
  Edit3,
  Check,
  AlertCircle,
  Eye,
  FileText,
  X
} from 'lucide-react';
import { Project, ContentDraft, ReelData, ReelScene } from '../../types';
import { api } from '../../services/api';

interface VideoReelTabProps {
  project: Project;
  draft: ContentDraft | null;
  onRefresh: () => void;
}

export const VideoReelTab: React.FC<VideoReelTabProps> = ({
  project,
  draft,
  onRefresh,
}) => {
  const [isRendering, setIsRendering] = useState<boolean>(false);
  const [isUpdatingConfig, setIsUpdatingConfig] = useState<boolean>(false);
  const [regeneratingSceneNum, setRegeneratingSceneNum] = useState<number | null>(null);
  const [editingSceneNum, setEditingSceneNum] = useState<number | null>(null);
  const [editedNarration, setEditedNarration] = useState<string>('');
  const [editedSubtitle, setEditedSubtitle] = useState<string>('');
  const [previewingSceneVideo, setPreviewingSceneVideo] = useState<{
    sceneNumber: number;
    url: string;
    title: string;
    duration: number;
  } | null>(null);
  const [showManifestModal, setShowManifestModal] = useState<boolean>(false);

  const reelData: ReelData = draft?.reel_data || {
    reel_title: project.title ? `Clinical Translation: ${project.title}` : 'Clinical Research Reel',
    hook: project.claims?.[0]?.claim_text ? `What does clinical research show about ${project.title}?` : 'Explore the peer-reviewed evidence.',
    target_duration_seconds: 30,
    mode: 'everyday',
    visual_style: 'talking_characters',
    language: 'en',
    voice_name: 'en-IN-NeerjaNeural',
    practical_takeaway: 'Peer-reviewed evidence translated for real-world lifestyle protection.',
    scenes: []
  };

  const currentMode = reelData.mode || 'everyday';
  const currentStyle = reelData.visual_style || 'talking_characters';
  const currentTheme = reelData.visual_theme || 'warm_editorial';
  const currentLang = reelData.language || 'en';
  const currentVoice = reelData.voice_name || 'en-IN-NeerjaNeural';
  const scenes: ReelScene[] = reelData.scenes || [];

  const videoArtifact = project.artifacts.find((a) => a.artifact_type === 'reel_video');
  const manifestData = reelData.manifest;
  const totalDuration = manifestData?.total_duration_seconds ?? scenes.reduce((acc, s) => acc + (s.duration_seconds || 5.0), 0);

  // Available options
  const visualStyles = [
    {
      id: 'talking_characters',
      label: 'Talking Characters',
      icon: '🍎',
      desc: '3D glossy Apple character, cute pink Gut, friendly microbes, & human cartoon characters'
    },
    {
      id: 'inside_your_body',
      label: 'Inside Your Body',
      icon: '🩸',
      desc: 'Finding-driven biology: Bloodstream red blood cell, Brain satiety synapse, & Stomach gastric emptying'
    },
    {
      id: 'everyday_human',
      label: 'Everyday Human',
      icon: '🚶',
      desc: 'Relatable dinner table, buzzing smartwatch alert, terrace walking strides, & ticking clock'
    },
    {
      id: 'animated_explainer',
      label: 'Animated Explainer',
      icon: '📊',
      desc: 'Dynamic 24fps CGM glucose curve, comparative bar spikes, and pulsing -34% drop badge'
    }
  ];

  const visualThemes = [
    {
      id: 'warm_editorial',
      label: 'Warm Editorial',
      desc: 'Terracotta & warm parchment paper tones',
      preview: ['#C85A32', '#FAF5EE', '#2C1E18']
    },
    {
      id: 'colourful_cartoon',
      label: 'Colourful Cartoon',
      desc: 'Vibrant indigo, electric orange & sunny yellow',
      preview: ['#4F46E5', '#FFF7CC', '#F97316']
    },
    {
      id: 'playful_pastel',
      label: 'Playful Pastel',
      desc: 'Dreamy soft lavender, violet & rose pastels',
      preview: ['#A855F7', '#F5F0FF', '#EC4899']
    },
    {
      id: 'cinematic',
      label: 'Cinematic Dark',
      desc: 'Moody obsidian dark mode with glowing cyan',
      preview: ['#0F172A', '#06B6D4', '#F59E0B']
    },
    {
      id: 'clean_infographic',
      label: 'Clean Infographic',
      desc: 'Clinical cobalt, crisp ice white & clear gray',
      preview: ['#0284C7', '#F0F9FF', '#0D9488']
    },
    {
      id: 'steer_brand',
      label: 'Steer Classic',
      desc: 'Authoritative cream, rust-orange & maroon',
      preview: ['#C04E2A', '#F5EBDF', '#661414']
    }
  ];

  const languages = [
    { id: 'en', label: 'English', native: 'Indian English', flag: '🇮🇳' },
    { id: 'hi', label: 'Hindi / Hinglish', native: 'हिन्दी + English', flag: '🇮🇳' },
    { id: 'te', label: 'Telugu + English', native: 'తెలుగు + English', flag: '🇮🇳' },
    { id: 'ta', label: 'Tamil + English', native: 'தமிழ் + English', flag: '🇮🇳' },
    { id: 'kn', label: 'Kannada + English', native: 'ಕನ್ನಡ + English', flag: '🇮🇳' },
    { id: 'ml', label: 'Malayalam + English', native: 'മലയാളം + English', flag: '🇮🇳' },
  ];

  const handleUpdateConfig = async (newMode: string, newStyle: string, newLang: string, newTheme?: string) => {
    setIsUpdatingConfig(true);
    const themeToUse = newTheme || currentTheme;
    try {
      await api.updateReelConfig(project.id, {
        mode: newMode,
        visual_style: newStyle,
        language: newLang,
        visual_theme: themeToUse
      });
      setIsUpdatingConfig(false);
      onRefresh();
    } catch (err: any) {
      setIsUpdatingConfig(false);
      alert(`Failed to update reel configuration: ${err.message}`);
    }
  };

  const handleRenderReel = async () => {
    setIsRendering(true);
    try {
      await api.generateReel(project.id);
      setIsRendering(false);
      onRefresh();
    } catch (err: any) {
      setIsRendering(false);
      alert(`Reel video rendering failed: ${err.message}`);
    }
  };

  const handleRegenerateScene = async (sceneNum: number) => {
    setRegeneratingSceneNum(sceneNum);
    try {
      await api.regenerateScene(project.id, sceneNum);
      setRegeneratingSceneNum(null);
      onRefresh();
    } catch (err: any) {
      setRegeneratingSceneNum(null);
      alert(`Failed to regenerate scene ${sceneNum}: ${err.message}`);
    }
  };

  const handleSaveSceneEdit = async (sceneNum: number) => {
    setRegeneratingSceneNum(sceneNum);
    try {
      await api.regenerateScene(project.id, sceneNum, {
        narration: editedNarration,
        subtitle_text: editedSubtitle
      });
      setEditingSceneNum(null);
      setRegeneratingSceneNum(null);
      onRefresh();
    } catch (err: any) {
      setRegeneratingSceneNum(null);
      alert(`Failed to save and re-render scene: ${err.message}`);
    }
  };

  const getSceneIcon = (scene: ReelScene) => {
    if (scene.organ_character === 'red_blood_cell') return '🩸';
    if (scene.organ_character === 'brain') return '🧠';
    if (scene.organ_character === 'stomach') return '🫀';
    if (scene.visual_style === 'inside_your_body') return '🔬';
    if (scene.scene_number === 1) return '🍎';
    if (scene.scene_number === 2) return '🍏';
    if (scene.scene_number === 3) return '🦠';
    if (scene.scene_number === 4) return '🥗';
    if (scene.scene_number === 5) return '✅';
    if (scene.scene_number === 6) return '🥤';
    return '🌟';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Top Banner & Reel Action Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-rust)', textTransform: 'uppercase' }}>
              ANIMATED 9:16 REEL STUDIO
            </span>
            <span className="badge-tag badge-blush">
              1080 × 1920 VERTICAL (24 FPS)
            </span>
            <span className="badge-tag badge-rust">
              {totalDuration.toFixed(1)} SECONDS
            </span>
            <span className={`badge-tag ${currentMode === 'professional' ? 'badge-maroon' : 'badge-approved'}`} style={{ fontSize: '11px' }}>
              {currentMode === 'professional' ? '🔬 PROFESSIONAL EVIDENCE MODE' : '✨ EVERYDAY ANIMATED MODE'}
            </span>
            {manifestData && (
              <span className="badge-tag badge-approved" style={{ fontSize: '11px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <CheckCircle2 size={12} />
                <span>AUTHORITATIVE MANIFEST VERIFIED</span>
              </span>
            )}
          </div>
          <h3 style={{ fontSize: '22px', color: 'var(--color-ink)', marginTop: '6px' }}>
            {reelData.reel_title}
          </h3>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {manifestData && (
            <button
              type="button"
              onClick={() => setShowManifestModal(true)}
              className="btn-secondary"
              style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px' }}
            >
              <FileText size={16} />
              <span>Inspect Manifest</span>
            </button>
          )}

          {videoArtifact && (
            <a
              href={api.getArtifactFileUrl(videoArtifact.id, true)}
              download
              className="btn-secondary"
              style={{ display: 'flex', alignItems: 'center', gap: '6px', textDecoration: 'none' }}
            >
              <Download size={16} />
              <span>Download MP4</span>
            </a>
          )}

          <button
            type="button"
            onClick={handleRenderReel}
            disabled={isRendering || isUpdatingConfig}
            className="btn-primary"
            style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            <RotateCw size={16} className={isRendering ? 'pulse-glow' : ''} />
            <span>{isRendering ? 'Rendering 24fps MP4...' : videoArtifact ? 'Re-Render Full Reel' : 'Render 24fps Animated Reel'}</span>
          </button>
        </div>
      </div>

      {/* Mode & Creative Configuration Panel */}
      <div className="steer-card" style={{ padding: '20px 24px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: currentMode === 'professional' ? '1fr 2fr' : '1fr 1.6fr 1.6fr', gap: '20px', alignItems: 'start' }}>
          
          {/* 1. Mode Switcher (Everyday vs Professional) */}
          <div>
            <label style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', display: 'block', marginBottom: '8px' }}>
              Storytelling Mode
            </label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <button
                type="button"
                onClick={() => handleUpdateConfig('everyday', currentStyle === 'professional' ? 'talking_characters' : currentStyle, currentLang, currentTheme)}
                disabled={isUpdatingConfig}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '10px 14px',
                  borderRadius: 'var(--radius-sm)',
                  border: currentMode === 'everyday' ? '2px solid var(--color-rust)' : '1px solid var(--color-blush)',
                  background: currentMode === 'everyday' ? '#FFF4EE' : '#FFFFFF',
                  color: currentMode === 'everyday' ? 'var(--color-rust)' : 'var(--color-ink)',
                  fontWeight: currentMode === 'everyday' ? 700 : 500,
                  fontSize: '13px',
                  cursor: 'pointer',
                  textAlign: 'left'
                }}
              >
                <Sparkles size={18} />
                <div>
                  <div>Everyday Mode</div>
                  <div style={{ fontSize: '10px', color: 'var(--color-clay)', fontWeight: 400 }}>Entertaining character-driven reels for Instagram</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleUpdateConfig('professional', 'professional', currentLang, currentTheme)}
                disabled={isUpdatingConfig}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '10px 14px',
                  borderRadius: 'var(--radius-sm)',
                  border: currentMode === 'professional' ? '2px solid var(--color-maroon)' : '1px solid var(--color-blush)',
                  background: currentMode === 'professional' ? '#FBF0EE' : '#FFFFFF',
                  color: currentMode === 'professional' ? 'var(--color-maroon)' : 'var(--color-ink)',
                  fontWeight: currentMode === 'professional' ? 700 : 500,
                  fontSize: '13px',
                  cursor: 'pointer',
                  textAlign: 'left'
                }}
              >
                <Activity size={18} />
                <div>
                  <div>Professional Mode</div>
                  <div style={{ fontSize: '10px', color: 'var(--color-clay)', fontWeight: 400 }}>Evidence-based clinical briefing with trial data</div>
                </div>
              </button>
            </div>
          </div>

          {/* 2. Visual Style Selector (Active in Everyday Mode) */}
          {currentMode === 'everyday' && (
            <div>
              <label style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', display: 'block', marginBottom: '8px' }}>
                Creative Visual Style
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                {visualStyles.map((vs) => (
                  <button
                    key={vs.id}
                    type="button"
                    onClick={() => handleUpdateConfig('everyday', vs.id, currentLang, currentTheme)}
                    disabled={isUpdatingConfig}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      padding: '8px 12px',
                      borderRadius: 'var(--radius-sm)',
                      border: currentStyle === vs.id ? '2px solid var(--color-rust)' : '1px solid var(--color-blush)',
                      background: currentStyle === vs.id ? '#FFF4EE' : '#FFFFFF',
                      color: currentStyle === vs.id ? 'var(--color-rust)' : 'var(--color-ink)',
                      fontWeight: currentStyle === vs.id ? 700 : 500,
                      fontSize: '11px',
                      cursor: 'pointer',
                      textAlign: 'left'
                    }}
                  >
                    <span style={{ fontSize: '16px' }}>{vs.icon}</span>
                    <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{vs.label}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* 3. Regional Language Selector */}
          <div>
            <label style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', display: 'block', marginBottom: '8px' }}>
              Spoken Regional Language & LocalVoice
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '6px' }}>
              {languages.map((lng) => (
                <button
                  key={lng.id}
                  type="button"
                  onClick={() => handleUpdateConfig(currentMode, currentStyle, lng.id, currentTheme)}
                  disabled={isUpdatingConfig}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    padding: '6px 8px',
                    borderRadius: 'var(--radius-sm)',
                    border: currentLang === lng.id ? '2px solid var(--color-rust)' : '1px solid var(--color-blush)',
                    background: currentLang === lng.id ? '#FFF4EE' : '#FFFFFF',
                    color: currentLang === lng.id ? 'var(--color-rust)' : 'var(--color-ink)',
                    fontSize: '11px',
                    cursor: 'pointer'
                  }}
                >
                  <span style={{ fontWeight: 700 }}>{lng.native}</span>
                  <span style={{ fontSize: '10px', color: 'var(--color-clay)' }}>{lng.label}</span>
                </button>
              ))}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--color-clay)', marginTop: '6px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Volume2 size={12} />
              <span>Voice: <strong>{currentVoice}</strong> (Natural pacing, scientific terminology preserved)</span>
            </div>
          </div>
        </div>

        {/* 4. AI-Generated Reel Background & Visual Theme Selector */}
        <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--color-blush)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px', flexWrap: 'wrap', gap: '8px' }}>
            <div>
              <label style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', display: 'block' }}>
                Reel Background & Visual Palette
              </label>
              <div style={{ fontSize: '12px', color: 'var(--color-ink)' }}>
                Configures palette, background contrast, and character styling in the rendered 24fps MP4
              </div>
            </div>
            <span className="badge-tag badge-blush" style={{ fontSize: '11px', textTransform: 'uppercase' }}>
              Active Theme: {visualThemes.find(t => t.id === currentTheme)?.label || currentTheme}
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '10px' }}>
            {visualThemes.map((theme) => {
              const isSelected = currentTheme === theme.id;
              return (
                <button
                  key={theme.id}
                  type="button"
                  onClick={() => handleUpdateConfig(currentMode, currentStyle, currentLang, theme.id)}
                  disabled={isUpdatingConfig}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                    padding: '10px 12px',
                    borderRadius: 'var(--radius-sm)',
                    border: isSelected ? '2px solid var(--color-rust)' : '1px solid var(--color-blush)',
                    background: isSelected ? '#FFF4EE' : '#FFFFFF',
                    color: isSelected ? 'var(--color-rust)' : 'var(--color-ink)',
                    cursor: 'pointer',
                    textAlign: 'left',
                    transition: 'all 0.15s ease'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontWeight: 700, fontSize: '12px' }}>{theme.label}</span>
                    <div style={{ display: 'flex', gap: '3px' }}>
                      {theme.preview.map((color, cIdx) => (
                        <div
                          key={cIdx}
                          style={{
                            width: '12px',
                            height: '12px',
                            borderRadius: '50%',
                            background: color,
                            border: '1px solid rgba(0,0,0,0.1)'
                          }}
                        />
                      ))}
                    </div>
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--color-clay)', lineHeight: '1.3' }}>
                    {theme.desc}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Studio Workspace: 9:16 Video Player Phone & Scene Storyboard */}
      <div style={{ display: 'grid', gridTemplateColumns: '380px 1fr', gap: '32px' }}>
        {/* Left Column: Phone Player Preview */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <div style={{
            width: '360px',
            background: 'var(--color-ink)',
            borderRadius: '40px',
            padding: '12px',
            boxShadow: '0 24px 60px rgba(53, 29, 29, 0.25)',
            border: '4px solid var(--color-ink)'
          }}>
            {/* Top speaker bar */}
            <div style={{ width: '80px', height: '4px', background: 'rgba(255,255,255,0.3)', borderRadius: '2px', margin: '4px auto 10px' }} />

            {/* Reel Screen (9:16 Aspect Ratio) */}
            <div style={{
              width: '100%',
              aspectRatio: '9 / 16',
              borderRadius: '28px',
              overflow: 'hidden',
              background: '#000000',
              position: 'relative',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              {videoArtifact ? (
                /* Actual Assembled Vertical MP4 Video Player! */
                <video
                  key={videoArtifact.id + (videoArtifact.file_size_bytes || 0)}
                  controls
                  autoPlay={false}
                  playsInline
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  src={api.getArtifactFileUrl(videoArtifact.id)}
                >
                  Your browser does not support vertical MP4 video playback.
                </video>
              ) : (
                /* Animated Placeholder Before Render */
                <div style={{
                  padding: '32px 24px',
                  height: '100%',
                  width: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  background: 'linear-gradient(180deg, #F8F2EB 0%, #F5EBDF 100%)',
                  textAlign: 'center'
                }}>
                  <div>
                    <div className="badge-tag badge-blush" style={{ fontSize: '10px', margin: '0 auto 16px' }}>
                      {currentMode === 'professional' ? 'CLINICAL BRIEFING' : 'ANIMATED REEL'}
                    </div>
                    <div style={{ fontFamily: 'var(--font-serif)', fontSize: '20px', fontWeight: 700, color: 'var(--color-ink)', lineHeight: 1.3, marginBottom: '14px' }}>
                      {reelData.hook}
                    </div>
                  </div>

                  <div style={{
                    width: '68px',
                    height: '68px',
                    borderRadius: '50%',
                    background: 'var(--color-rust)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    margin: '0 auto',
                    boxShadow: '0 4px 16px rgba(192, 78, 42, 0.35)',
                    color: '#FFFFFF'
                  }}>
                    <Video size={30} />
                  </div>

                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-ink)', marginBottom: '8px' }}>
                      Ready to render {currentLang.toUpperCase()} animated reel
                    </div>
                    <div style={{ fontSize: '11px', color: 'var(--color-clay)' }}>
                      Multi-frame 24fps motion, synced voiceover & high-contrast subtitles
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Video Metadata Chip */}
          {videoArtifact && (
            <div style={{
              width: '360px',
              marginTop: '14px',
              background: '#FFFFFF',
              border: '1px solid var(--color-blush)',
              borderRadius: 'var(--radius-md)',
              padding: '12px 16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <div>
                <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-ink)' }}>
                  Rendered MP4: {(videoArtifact.file_size_bytes / (1024 * 1024)).toFixed(1)} MB
                </div>
                <div style={{ fontSize: '11px', color: 'var(--color-clay)' }}>
                  1080×1920 • 24 FPS • H.264/AAC ({totalDuration.toFixed(1)}s)
                </div>
              </div>
              <span className="badge-tag badge-approved" style={{ fontSize: '10px' }}>
                READY TO SHARE
              </span>
            </div>
          )}
        </div>

        {/* Right Column: Scene-by-Scene Storyboard & Editor */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Reel Overview Card */}
          <div className="steer-card" style={{ padding: '20px 24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
              <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>
                {currentStyle === 'inside_your_body' ? 'Biological Findings Overview' : 'Opening Hook & Takeaway'}
              </span>
              <span style={{ fontSize: '12px', color: 'var(--color-rust)', fontWeight: 600 }}>
                {scenes.length} Validated Scenes • Total {totalDuration.toFixed(1)}s
              </span>
            </div>

            <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--color-ink)', marginBottom: '8px', lineHeight: 1.4 }}>
              "{reelData.hook}"
            </div>

            <div style={{ fontSize: '13px', color: 'var(--color-ink-muted)', lineHeight: 1.5 }}>
              <strong>Clinical Translation:</strong> {reelData.practical_takeaway}
            </div>
          </div>

          {/* Scene Storyboard Cards List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <h4 style={{ fontSize: '16px', color: 'var(--color-ink)', margin: 0 }}>
                Scene Storyboard & Visual Assets ({scenes.length} Scenes)
              </h4>
              <span style={{ fontSize: '12px', color: 'var(--color-clay)' }}>
                Authoritative Timeline: 00:00 → {Math.floor(totalDuration / 60).toString().padStart(2, '0')}:{(Math.round(totalDuration % 60)).toString().padStart(2, '0')}
              </span>
            </div>

            {scenes.map((scene, idx) => {
              const isEditing = editingSceneNum === scene.scene_number;
              const isRegen = regeneratingSceneNum === scene.scene_number;
              const sceneThumbUrl = scene.thumbnail_url 
                ? (scene.thumbnail_url.startsWith('http') ? scene.thumbnail_url : `http://127.0.0.1:8000${scene.thumbnail_url}`)
                : api.getReelSceneThumbnailUrl(project.id, scene.scene_number);
              const sceneVideoUrl = scene.video_url
                ? (scene.video_url.startsWith('http') ? scene.video_url : `http://127.0.0.1:8000${scene.video_url}`)
                : api.getReelSceneVideoUrl(project.id, scene.scene_number);

              const timeRangeDisplay = scene.time_range 
                ? scene.time_range 
                : `${(scene.start_time_seconds ?? (idx * 5.0)).toFixed(1)}s - ${(scene.end_time_seconds ?? ((idx + 1) * 5.0)).toFixed(1)}s`;

              return (
                <div
                  key={scene.scene_number || idx}
                  className="steer-card"
                  style={{
                    padding: '20px 24px',
                    borderLeft: `4px solid var(--color-rust)`
                  }}
                >
                  {/* Scene Header */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px', flexWrap: 'wrap', gap: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <span style={{
                        fontFamily: 'monospace',
                        fontWeight: 700,
                        fontSize: '13px',
                        background: 'var(--color-cream)',
                        padding: '3px 8px',
                        borderRadius: '6px',
                        color: 'var(--color-rust)'
                      }}>
                        SCENE {scene.scene_number || idx + 1}
                      </span>
                      <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-ink)' }}>
                        ⏱️ {timeRangeDisplay} ({scene.duration_seconds.toFixed(1)}s)
                      </span>
                      {scene.organ_character && (
                        <span className="badge-tag badge-maroon" style={{ fontSize: '10px' }}>
                          ORGAN: {scene.organ_character.replace('_', ' ').toUpperCase()}
                        </span>
                      )}
                      <span className="badge-tag badge-blush" style={{ fontSize: '10px' }}>
                        {scene.visual_style || currentStyle}
                      </span>
                      {videoArtifact ? (
                        <span className="badge-tag badge-approved" style={{ fontSize: '10px', display: 'flex', alignItems: 'center', gap: '3px' }}>
                          <CheckCircle2 size={10} />
                          <span>RENDERED</span>
                        </span>
                      ) : (
                        <span className="badge-tag badge-blush" style={{ fontSize: '10px' }}>
                          READY TO RENDER
                        </span>
                      )}
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      {scene.claim_ids && scene.claim_ids.map((cid) => (
                        <span key={cid} style={{ background: 'var(--color-rust-light)', color: 'var(--color-rust)', fontSize: '11px', fontWeight: 700, padding: '2px 8px', borderRadius: '4px' }}>
                          {cid}
                        </span>
                      ))}

                      {!isEditing ? (
                        <>
                          <button
                            type="button"
                            onClick={() => {
                              setEditingSceneNum(scene.scene_number);
                              setEditedNarration(scene.narration);
                              setEditedSubtitle(scene.subtitle_text || scene.narration);
                            }}
                            className="btn-secondary"
                            style={{ padding: '4px 10px', fontSize: '11px' }}
                          >
                            <Edit3 size={12} />
                            <span>Edit Script</span>
                          </button>
                          <button
                            type="button"
                            onClick={() => handleRegenerateScene(scene.scene_number)}
                            disabled={isRegen}
                            className="btn-secondary"
                            style={{ padding: '4px 10px', fontSize: '11px' }}
                            title="Regenerate this individual scene"
                          >
                            <RotateCw size={12} className={isRegen ? 'pulse-glow' : ''} />
                            <span>{isRegen ? 'Rendering...' : 'Regen Scene'}</span>
                          </button>
                        </>
                      ) : (
                        <>
                          <button
                            type="button"
                            onClick={() => handleSaveSceneEdit(scene.scene_number)}
                            disabled={isRegen}
                            className="btn-primary"
                            style={{ padding: '4px 12px', fontSize: '11px' }}
                          >
                            <Check size={12} />
                            <span>{isRegen ? 'Saving & Rendering...' : 'Save & Re-Render'}</span>
                          </button>
                          <button
                            type="button"
                            onClick={() => setEditingSceneNum(null)}
                            className="btn-secondary"
                            style={{ padding: '4px 10px', fontSize: '11px' }}
                          >
                            <span>Cancel</span>
                          </button>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Scene Body: Visual Thumbnail Preview + Script Details */}
                  <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '16px', alignItems: 'start' }}>
                    
                    {/* Scene Visual Asset Preview Box (9:16 Aspect) */}
                    <div style={{
                      width: '120px',
                      aspectRatio: '9 / 16',
                      borderRadius: '12px',
                      overflow: 'hidden',
                      background: 'var(--color-cream)',
                      border: '1px solid var(--color-blush)',
                      position: 'relative',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
                    }}>
                      {videoArtifact ? (
                        <>
                          <img
                            src={sceneThumbUrl}
                            alt={scene.on_screen_text}
                            onError={(e) => {
                              // If individual thumb fails, hide img and show fallback icon
                              (e.target as HTMLElement).style.display = 'none';
                            }}
                            style={{
                              width: '100%',
                              height: '100%',
                              objectFit: 'cover'
                            }}
                          />
                          {/* Play Scene Button Overlay */}
                          <button
                            type="button"
                            onClick={() => setPreviewingSceneVideo({
                              sceneNumber: scene.scene_number,
                              url: sceneVideoUrl,
                              title: scene.on_screen_text,
                              duration: scene.duration_seconds
                            })}
                            style={{
                              position: 'absolute',
                              bottom: '8px',
                              background: 'rgba(53, 29, 29, 0.85)',
                              color: '#FFFFFF',
                              border: 'none',
                              borderRadius: '20px',
                              padding: '4px 8px',
                              fontSize: '10px',
                              fontWeight: 600,
                              cursor: 'pointer',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '4px',
                              backdropFilter: 'blur(4px)'
                            }}
                          >
                            <Play size={10} fill="#FFFFFF" />
                            <span>Preview</span>
                          </button>
                        </>
                      ) : (
                        <div style={{ textAlign: 'center', padding: '10px' }}>
                          <span style={{ fontSize: '28px', display: 'block', marginBottom: '6px' }}>
                            {getSceneIcon(scene)}
                          </span>
                          <span style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-clay)' }}>
                            SCENE {scene.scene_number}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Scene Script & Cues Content */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                        <div style={{ background: 'var(--color-cream)', padding: '10px 14px', borderRadius: 'var(--radius-sm)' }}>
                          <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', marginBottom: '2px' }}>
                            On-Screen Headline Text
                          </div>
                          <div style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-ink)' }}>
                            {scene.on_screen_text}
                          </div>
                        </div>

                        <div style={{ background: 'var(--color-cream)', padding: '10px 14px', borderRadius: 'var(--radius-sm)' }}>
                          <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', marginBottom: '2px' }}>
                            Visual Action & Animation Cue
                          </div>
                          <div style={{ fontSize: '12px', color: 'var(--color-ink)', fontStyle: 'italic' }}>
                            {scene.visual_cue}
                          </div>
                        </div>
                      </div>

                      {/* Spoken Narration & Subtitle */}
                      <div style={{ background: '#FFF9F4', border: '1px solid var(--color-blush)', borderRadius: 'var(--radius-sm)', padding: '12px 16px' }}>
                        <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-rust)', textTransform: 'uppercase', marginBottom: '4px' }}>
                          Spoken Narration & Timed Subtitles ({currentLang.toUpperCase()})
                        </div>
                        
                        {!isEditing ? (
                          <div>
                            <div style={{ fontSize: '13px', color: 'var(--color-ink)', lineHeight: 1.5, marginBottom: '6px' }}>
                              "{scene.narration}"
                            </div>
                            <div style={{ fontSize: '11px', color: 'var(--color-clay)', fontStyle: 'italic' }}>
                              Subtitles: "{scene.subtitle_text || scene.narration}"
                            </div>
                          </div>
                        ) : (
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '6px' }}>
                            <div>
                              <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-ink-muted)', display: 'block', marginBottom: '4px' }}>
                                Spoken Narration Text
                              </label>
                              <textarea
                                value={editedNarration}
                                onChange={(e) => setEditedNarration(e.target.value)}
                                rows={3}
                                style={{
                                  width: '100%',
                                  padding: '8px 10px',
                                  borderRadius: 'var(--radius-sm)',
                                  border: '1px solid var(--color-clay)',
                                  fontSize: '13px',
                                  fontFamily: 'inherit'
                                }}
                              />
                            </div>

                            <div>
                              <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-ink-muted)', display: 'block', marginBottom: '4px' }}>
                                Subtitle Overlay Text
                              </label>
                              <input
                                type="text"
                                value={editedSubtitle}
                                onChange={(e) => setEditedSubtitle(e.target.value)}
                                style={{
                                  width: '100%',
                                  padding: '8px 10px',
                                  borderRadius: 'var(--radius-sm)',
                                  border: '1px solid var(--color-clay)',
                                  fontSize: '13px',
                                  fontFamily: 'inherit'
                                }}
                              />
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Modal: Single Scene MP4 Video Player */}
      {previewingSceneVideo && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(53, 29, 29, 0.75)',
          backdropFilter: 'blur(6px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: '#FFFFFF',
            borderRadius: '24px',
            padding: '24px',
            maxWidth: '420px',
            width: '90%',
            boxShadow: '0 20px 50px rgba(0,0,0,0.3)',
            display: 'flex',
            flexDirection: 'column',
            gap: '16px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <h4 style={{ margin: 0, fontSize: '16px', color: 'var(--color-ink)' }}>
                  Scene {previewingSceneVideo.sceneNumber} Preview
                </h4>
                <div style={{ fontSize: '12px', color: 'var(--color-clay)' }}>
                  {previewingSceneVideo.title} • {previewingSceneVideo.duration.toFixed(1)}s
                </div>
              </div>
              <button
                type="button"
                onClick={() => setPreviewingSceneVideo(null)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '4px',
                  color: 'var(--color-clay)'
                }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{
              width: '100%',
              aspectRatio: '9 / 16',
              borderRadius: '16px',
              overflow: 'hidden',
              background: '#000000'
            }}>
              <video
                controls
                autoPlay
                playsInline
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                src={previewingSceneVideo.url}
              >
                Your browser does not support vertical MP4 video playback.
              </video>
            </div>

            <button
              type="button"
              onClick={() => setPreviewingSceneVideo(null)}
              className="btn-secondary"
              style={{ width: '100%' }}
            >
              Close Scene Preview
            </button>
          </div>
        </div>
      )}

      {/* Modal: Authoritative Render Manifest Inspector */}
      {showManifestModal && manifestData && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(53, 29, 29, 0.75)',
          backdropFilter: 'blur(6px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: '#FFFFFF',
            borderRadius: '24px',
            padding: '28px',
            maxWidth: '680px',
            width: '90%',
            maxHeight: '85vh',
            overflowY: 'auto',
            boxShadow: '0 20px 50px rgba(0,0,0,0.3)',
            display: 'flex',
            flexDirection: 'column',
            gap: '18px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileText size={20} color="var(--color-rust)" />
                <h3 style={{ margin: 0, fontSize: '18px', color: 'var(--color-ink)' }}>
                  Authoritative Render Manifest
                </h3>
              </div>
              <button
                type="button"
                onClick={() => setShowManifestModal(false)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '4px',
                  color: 'var(--color-clay)'
                }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ fontSize: '13px', color: 'var(--color-ink-muted)' }}>
              This render manifest authoritatively governs the MP4 timeline, scene timestamps, and codecs. Scene durations are derived from actual audio synthesis rather than hardcoded approximations.
            </div>

            {/* Codecs & Summary Table */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '12px',
              background: 'var(--color-cream)',
              padding: '16px',
              borderRadius: 'var(--radius-sm)'
            }}>
              <div>
                <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>Total Duration</div>
                <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--color-rust)' }}>{manifestData.total_duration_seconds?.toFixed(2)}s</div>
              </div>
              <div>
                <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>Resolution</div>
                <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--color-ink)' }}>{manifestData.resolution || '1080×1920'}</div>
              </div>
              <div>
                <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>Framerate</div>
                <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--color-ink)' }}>{manifestData.fps || 24} FPS</div>
              </div>
              <div>
                <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>Codecs</div>
                <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--color-ink)' }}>H.264 / AAC</div>
              </div>
            </div>

            {/* Scene Timeline Table */}
            <div>
              <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', marginBottom: '8px' }}>
                Timeline Breakdown by Scene
              </div>
              <div style={{ border: '1px solid var(--color-blush)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px', textAlign: 'left' }}>
                  <thead style={{ background: 'var(--color-soft-paper)', borderBottom: '1px solid var(--color-blush)' }}>
                    <tr>
                      <th style={{ padding: '8px 12px' }}>#</th>
                      <th style={{ padding: '8px 12px' }}>Start</th>
                      <th style={{ padding: '8px 12px' }}>End</th>
                      <th style={{ padding: '8px 12px' }}>Duration</th>
                      <th style={{ padding: '8px 12px' }}>Frames</th>
                      <th style={{ padding: '8px 12px' }}>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(manifestData.scenes || []).map((ms: any, i: number) => (
                      <tr key={i} style={{ borderBottom: '1px solid var(--color-blush)' }}>
                        <td style={{ padding: '8px 12px', fontWeight: 700 }}>Scene {ms.scene_number || i + 1}</td>
                        <td style={{ padding: '8px 12px' }}>{ms.start_time_seconds?.toFixed(1)}s</td>
                        <td style={{ padding: '8px 12px' }}>{ms.end_time_seconds?.toFixed(1)}s</td>
                        <td style={{ padding: '8px 12px', fontWeight: 600 }}>{ms.duration_seconds?.toFixed(1)}s</td>
                        <td style={{ padding: '8px 12px' }}>{ms.total_frames || Math.round(ms.duration_seconds * 24)}</td>
                        <td style={{ padding: '8px 12px' }}>
                          <span className="badge-tag badge-approved" style={{ fontSize: '9px' }}>
                            {ms.render_status || 'completed'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <button
              type="button"
              onClick={() => setShowManifestModal(false)}
              className="btn-primary"
              style={{ width: '100%' }}
            >
              Close Manifest
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
