import React, { useState } from 'react';
import { Download, RotateCw, Image as ImageIcon, Edit3, Check, Save } from 'lucide-react';
import { Project, ContentDraft, StaticData } from '../../types';
import { api } from '../../services/api';

interface StaticPostTabProps {
  project: Project;
  draft: ContentDraft | null;
  onRefresh: () => void;
}

export const StaticPostTab: React.FC<StaticPostTabProps> = ({
  project,
  draft,
  onRefresh,
}) => {
  const [isRendering, setIsRendering] = useState<boolean>(false);
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [editedPost, setEditedPost] = useState<StaticData | null>(null);

  const staticData: StaticData = draft?.static_data || {
    eyebrow: 'DOCTOR-LED METABOLIC INSIGHT',
    headline: project.title ? `Clinical Translation: ${project.title}` : 'Awaiting research processing...',
    body_copy: project.paper_metadata?.key_findings?.[0] || 'Process paper evidence to generate verified post copy.',
    practical_takeaway: 'Grounded in peer-reviewed clinical research.',
    badge: 'Steer Clinical Standard',
    source_citation: project.paper_metadata?.journal ? `${project.paper_metadata.journal}` : 'Verified Clinical Source',
    claim_ids: project.claims?.slice(0, 1).map((c) => c.claim_id) || [],
  };

  const artifact = project.artifacts.find((a) => a.artifact_type === 'static_post');

  const handleRender = async () => {
    setIsRendering(true);
    try {
      await api.generateStatic(project.id);
      setIsRendering(false);
      onRefresh();
    } catch (err: any) {
      setIsRendering(false);
      alert(`Static post rendering failed: ${err.message}`);
    }
  };

  const startEdit = () => {
    setEditedPost({ ...staticData });
    setIsEditing(true);
  };

  const saveEdit = async () => {
    if (!draft || !editedPost) return;
    try {
      await api.updateDraft(project.id, { static_data: editedPost });
      setIsEditing(false);
      onRefresh();
    } catch (err: any) {
      alert(`Failed to save static post changes: ${err.message}`);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Top action bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-rust)', textTransform: 'uppercase' }}>
              STATIC INSTAGRAM POST
            </span>
            <span className="badge-tag badge-blush">
              1080 × 1350 PORTRAIT
            </span>
            <span className="badge-tag badge-rust">
              HIGH IMPACT
            </span>
          </div>
          <h3 style={{ fontSize: '22px', color: 'var(--color-ink)', marginTop: '4px' }}>
            Single Statement Hero Graphic
          </h3>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button
            onClick={handleRender}
            disabled={isRendering}
            className="btn-primary"
            style={{ fontSize: '13px', padding: '9px 18px' }}
          >
            <RotateCw size={15} className={isRendering ? 'pulse-glow' : ''} />
            <span>{isRendering ? 'Rendering 1080x1350 PNG...' : 'Render Static Post PNG'}</span>
          </button>

          {artifact && (
            <a
              href={api.getArtifactFileUrl(artifact.id, true)}
              className="btn-secondary"
              style={{ fontSize: '13px', padding: '8px 16px' }}
              download
            >
              <Download size={16} />
              <span>Download PNG</span>
            </a>
          )}
        </div>
      </div>

      {/* Main Studio Workspace: Phone Mockup + Copy Controls */}
      <div style={{ display: 'grid', gridTemplateColumns: '460px 1fr', gap: '32px' }}>
        {/* Phone Frame Preview */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <div style={{
            width: '380px',
            background: 'var(--color-ink)',
            borderRadius: '36px',
            padding: '12px',
            boxShadow: '0 24px 60px rgba(53, 29, 29, 0.22)',
            border: '4px solid var(--color-ink)'
          }}>
            <div style={{ width: '80px', height: '4px', background: 'rgba(255,255,255,0.3)', borderRadius: '2px', margin: '4px auto 10px' }} />

            <div style={{
              width: '100%',
              aspectRatio: '4 / 5',
              borderRadius: '24px',
              overflow: 'hidden',
              background: 'var(--color-soft-paper)',
              position: 'relative'
            }}>
              {artifact ? (
                <img
                  src={api.getArtifactFileUrl(artifact.id)}
                  alt="Static Post"
                  style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                />
              ) : (
                <div style={{
                  padding: '32px 24px',
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  background: 'var(--color-cream)',
                  border: '1px solid var(--color-blush)'
                }}>
                  <div>
                    <div className="badge-tag badge-blush" style={{ fontSize: '10px', marginBottom: '14px' }}>
                      {staticData.badge || 'STEER CLINICAL STANDARD'}
                    </div>

                    <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-rust)', textTransform: 'uppercase', marginBottom: '6px' }}>
                      {staticData.eyebrow || 'METABOLIC SCIENCE'}
                    </div>

                    <div style={{ fontFamily: 'var(--font-serif)', fontSize: '21px', fontWeight: 700, color: 'var(--color-ink)', lineHeight: 1.25, marginBottom: '16px' }}>
                      {staticData.headline}
                    </div>

                    <div style={{ width: '60px', height: '3px', background: 'var(--color-rust)', marginBottom: '16px' }} />

                    <div style={{ fontSize: '13px', color: 'var(--color-ink)', lineHeight: 1.5, marginBottom: '20px' }}>
                      {staticData.body_copy}
                    </div>

                    <div style={{
                      background: 'var(--color-soft-paper)',
                      border: '1px solid var(--color-clay)',
                      borderRadius: '12px',
                      padding: '12px 14px'
                    }}>
                      <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--color-rust)', textTransform: 'uppercase', marginBottom: '2px' }}>
                        STEER CLINICAL ACTION
                      </div>
                      <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-ink)' }}>
                        {staticData.practical_takeaway}
                      </div>
                    </div>
                  </div>

                  <div style={{ borderTop: '1px solid var(--color-card-border)', paddingTop: '10px', fontSize: '10px', color: 'var(--color-clay)' }}>
                    {staticData.source_citation || 'Steer Metabolic Health Club Protocol'}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Copy Editor */}
        <div className="steer-card" style={{ padding: '32px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '22px' }}>
            <div>
              <span className="badge-tag badge-rust" style={{ marginBottom: '6px' }}>
                EDITORIAL COPY
              </span>
              <h4 style={{ fontSize: '20px', color: 'var(--color-ink)' }}>Static Post Content & Layout</h4>
            </div>

            {!isEditing ? (
              <button onClick={startEdit} className="btn-secondary" style={{ fontSize: '13px', padding: '6px 14px' }}>
                <Edit3 size={14} />
                <span>Edit Copy</span>
              </button>
            ) : (
              <button onClick={saveEdit} className="btn-primary" style={{ fontSize: '13px', padding: '6px 16px' }}>
                <Check size={14} />
                <span>Save Changes</span>
              </button>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', marginBottom: '4px' }}>
                Eyebrow
              </label>
              {isEditing ? (
                <input
                  type="text"
                  value={editedPost?.eyebrow || ''}
                  onChange={(e) => setEditedPost(editedPost ? { ...editedPost, eyebrow: e.target.value } : null)}
                  style={{ width: '100%', padding: '8px 12px', borderRadius: '8px', border: '1px solid var(--color-clay)' }}
                />
              ) : (
                <div style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-rust)' }}>
                  {staticData.eyebrow}
                </div>
              )}
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', marginBottom: '4px' }}>
                Headline
              </label>
              {isEditing ? (
                <textarea
                  rows={2}
                  value={editedPost?.headline || ''}
                  onChange={(e) => setEditedPost(editedPost ? { ...editedPost, headline: e.target.value } : null)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid var(--color-clay)', fontSize: '15px' }}
                />
              ) : (
                <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--color-ink)' }}>
                  {staticData.headline}
                </div>
              )}
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', marginBottom: '4px' }}>
                Supporting Clinical Copy
              </label>
              {isEditing ? (
                <textarea
                  rows={4}
                  value={editedPost?.body_copy || ''}
                  onChange={(e) => setEditedPost(editedPost ? { ...editedPost, body_copy: e.target.value } : null)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid var(--color-clay)', fontSize: '14px' }}
                />
              ) : (
                <div style={{ fontSize: '15px', color: 'var(--color-ink)', lineHeight: 1.55 }}>
                  {staticData.body_copy}
                </div>
              )}
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', marginBottom: '4px' }}>
                Practical Steer Rule / Takeaway
              </label>
              {isEditing ? (
                <input
                  type="text"
                  value={editedPost?.practical_takeaway || ''}
                  onChange={(e) => setEditedPost(editedPost ? { ...editedPost, practical_takeaway: e.target.value } : null)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid var(--color-clay)' }}
                />
              ) : (
                <div style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-rust)' }}>
                  {staticData.practical_takeaway}
                </div>
              )}
            </div>

            <div style={{
              borderTop: '1px solid var(--color-card-border)',
              paddingTop: '14px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              fontSize: '12px',
              color: 'var(--color-clay)'
            }}>
              <div>Source: {staticData.source_citation || 'Steer Protocol'}</div>
              <div>
                Linked Claims:{' '}
                {staticData.claim_ids && staticData.claim_ids.map((id) => (
                  <span key={id} style={{ background: 'var(--color-cream)', padding: '2px 6px', borderRadius: '4px', marginLeft: '4px', fontWeight: 700, color: 'var(--color-rust)' }}>
                    {id}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
