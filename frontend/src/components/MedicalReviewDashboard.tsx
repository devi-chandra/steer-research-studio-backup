import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Edit3, 
  Quote, 
  Clock, 
  UserCheck, 
  AlertOctagon,
  FileCheck,
  Save,
  Layers,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { Project, Claim } from '../types';
import { api } from '../services/api';

interface MedicalReviewDashboardProps {
  project: Project;
  onClaimUpdated: () => void;
  selectedClaimId?: string | null;
}

export const MedicalReviewDashboard: React.FC<MedicalReviewDashboardProps> = ({
  project,
  onClaimUpdated,
  selectedClaimId,
}) => {
  const [activeClaimId, setActiveClaimId] = useState<string>(
    selectedClaimId || (project.claims && project.claims.length > 0 ? project.claims[0].claim_id : '')
  );
  const [reviewerRole, setReviewerRole] = useState<string>('Medical Reviewer');
  const [notes, setNotes] = useState<string>('');
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [editedText, setEditedText] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);
  const [crossFormatAudit, setCrossFormatAudit] = useState<any | null>(null);
  const [isLoadingAudit, setIsLoadingAudit] = useState<boolean>(false);
  const [showAuditDetails, setShowAuditDetails] = useState<boolean>(true);

  useEffect(() => {
    if (selectedClaimId) {
      setActiveClaimId(selectedClaimId);
    } else if (project.claims && project.claims.length > 0) {
      setActiveClaimId(project.claims[0].claim_id);
    } else {
      setActiveClaimId('');
    }
  }, [project.id, selectedClaimId, project.claims]);

  useEffect(() => {
    setIsLoadingAudit(true);
    api.getCrossFormatChecks(project.id)
      .then((data) => {
        setCrossFormatAudit(data);
        setIsLoadingAudit(false);
      })
      .catch((err) => {
        console.error('Cross-format check error:', err);
        setIsLoadingAudit(false);
      });
  }, [project.id]);

  const claims = project.claims || [];
  const currentClaim = claims.find((c) => c.claim_id === activeClaimId) || claims[0];

  const pendingCount = claims.filter((c) => c.verification_status === 'pending').length;
  const approvedCount = claims.filter((c) => c.verification_status === 'approved').length;
  const flaggedCount = claims.filter((c) => c.verification_status === 'flagged').length;
  const rejectedCount = claims.filter((c) => c.verification_status === 'rejected').length;

  const handleAction = async (action: 'approve' | 'reject' | 'flag' | 'edit') => {
    if (!currentClaim) return;
    setIsSubmitting(true);
    setActionSuccess(null);

    try {
      await api.reviewClaim(
        project.id,
        currentClaim.claim_id,
        action,
        notes.trim() || undefined,
        reviewerRole,
        action === 'edit' ? editedText.trim() : undefined
      );

      setIsSubmitting(false);
      setIsEditing(false);
      setNotes('');
      setActionSuccess(`Claim ${currentClaim.claim_id} marked as ${action.toUpperCase()} by ${reviewerRole}.`);
      onClaimUpdated();
      setTimeout(() => setActionSuccess(null), 4000);
    } catch (err: any) {
      setIsSubmitting(false);
      alert(`Review action failed: ${err.message}`);
    }
  };

  const startEdit = () => {
    if (currentClaim) {
      setEditedText(currentClaim.claim_text);
      setIsEditing(true);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Top Banner: Medical Review Compliance Gate */}
      <div className="steer-card" style={{
        padding: '24px 32px',
        background: pendingCount > 0 ? '#FFF9F4' : '#F4F9F4',
        border: `1px solid ${pendingCount > 0 ? 'var(--color-rust)' : '#A5D6A7'}`
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div style={{
              width: '46px',
              height: '46px',
              borderRadius: '50%',
              background: pendingCount > 0 ? 'var(--color-rust-light)' : '#E8F5E9',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: pendingCount > 0 ? 'var(--color-rust)' : '#1B5E20'
            }}>
              <ShieldCheck size={26} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h3 style={{ fontSize: '20px', color: 'var(--color-ink)' }}>
                  Human Medical Review Gate
                </h3>
                <span className={`badge-tag ${pendingCount > 0 ? 'badge-pending' : 'badge-approved'}`}>
                  {pendingCount > 0 ? `${pendingCount} CLAIMS PENDING SIGN-OFF` : 'ALL CLAIMS VERIFIED'}
                </span>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--color-ink-muted)', marginTop: '2px' }}>
                Steer safety protocol: AI drafts claims as pending review. Every factual health statement requires physician validation before public distribution.
              </p>
            </div>
          </div>

          {/* Quick reviewer role selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-ink-muted)' }}>
              Reviewer Role:
            </span>
            <select
              value={reviewerRole}
              onChange={(e) => setReviewerRole(e.target.value)}
              style={{
                padding: '8px 14px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-clay)',
                background: 'var(--color-white)',
                fontFamily: 'var(--font-sans)',
                fontSize: '13px',
                fontWeight: 600,
                color: 'var(--color-ink)'
              }}
            >
              <option value="Medical Reviewer">Medical Reviewer (Steer Club)</option>
              <option value="Senior Clinical Endocrinologist">Senior Clinical Endocrinologist</option>
              <option value="Chief Medical Officer">Chief Medical Officer</option>
              <option value="Test Reviewer (Hackathon Demo)">Test Reviewer (Hackathon Demo)</option>
            </select>
          </div>
        </div>

        {/* Status Count Pills */}
        <div style={{ display: 'flex', gap: '16px', marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--color-card-border)' }}>
          <div style={{ fontSize: '13px' }}>
            Total: <strong>{claims.length}</strong>
          </div>
          <div style={{ fontSize: '13px', color: '#1B5E20' }}>
            Approved: <strong>{approvedCount}</strong>
          </div>
          <div style={{ fontSize: '13px', color: '#E65100' }}>
            Pending Review: <strong>{pendingCount}</strong>
          </div>
          <div style={{ fontSize: '13px', color: '#BF360C' }}>
            Flagged: <strong>{flaggedCount}</strong>
          </div>
          <div style={{ fontSize: '13px', color: '#C62828' }}>
            Rejected: <strong>{rejectedCount}</strong>
          </div>
        </div>
      </div>

      {actionSuccess && (
        <div style={{
          background: '#E8F5E9',
          border: '1px solid #A5D6A7',
          color: '#1B5E20',
          borderRadius: 'var(--radius-md)',
          padding: '12px 18px',
          fontWeight: 600,
          fontSize: '14px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <CheckCircle size={18} />
          <span>{actionSuccess}</span>
        </div>
      )}

      {/* Cross-Format Claims Consistency Audit Gate */}
      {crossFormatAudit && (
        <div className="steer-card" style={{ padding: '22px 26px', borderLeft: '4px solid var(--color-rust)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', marginBottom: showAuditDetails ? '16px' : 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '8px',
                background: 'var(--color-cream)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--color-rust)'
              }}>
                <Layers size={18} />
              </div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <h4 style={{ margin: 0, fontSize: '15px', color: 'var(--color-ink)' }}>
                    Cross-Format Claim Consistency Audit
                  </h4>
                  <span className="badge-tag badge-approved" style={{ fontSize: '10px' }}>
                    {crossFormatAudit.summary?.passed_checks} / {crossFormatAudit.summary?.total_checks} CHECKS PASSED
                  </span>
                </div>
                <div style={{ fontSize: '12px', color: 'var(--color-clay)', marginTop: '2px' }}>
                  Cross-checks Carousel, Static Post, Animated Reel, and Captions against the Verified Evidence Ledger
                </div>
              </div>
            </div>

            <button
              type="button"
              onClick={() => setShowAuditDetails(!showAuditDetails)}
              className="btn-secondary"
              style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 12px', fontSize: '12px' }}
            >
              <span>{showAuditDetails ? 'Hide Audit Items' : 'View Audit Items'}</span>
              {showAuditDetails ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
          </div>

          {showAuditDetails && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px', marginTop: '14px', paddingTop: '14px', borderTop: '1px solid var(--color-blush)' }}>
              {crossFormatAudit.checks?.map((chk: any) => (
                <div
                  key={chk.check_id}
                  style={{
                    background: chk.status === 'passed' ? '#FBFDFB' : '#FFFDF9',
                    border: `1px solid ${chk.status === 'passed' ? '#C8E6C9' : '#FFE082'}`,
                    borderRadius: 'var(--radius-sm)',
                    padding: '12px 14px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '4px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-ink)' }}>
                      {chk.label}
                    </span>
                    <span
                      style={{
                        fontSize: '9px',
                        fontWeight: 700,
                        padding: '2px 6px',
                        borderRadius: '4px',
                        background: chk.status === 'passed' ? '#E8F5E9' : '#FFF8E1',
                        color: chk.status === 'passed' ? '#1B5E20' : '#E65100'
                      }}
                    >
                      {chk.status === 'passed' ? '✓ CONSISTENT' : '⚠ WARNING'}
                    </span>
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--color-ink-muted)', lineHeight: 1.4 }}>
                    {chk.details}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Main Review Workspace: Claim Selector + Detailed Review Workbench */}
      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '24px' }}>
        {/* Left Column: Claims Navigator */}
        <div className="steer-card" style={{ padding: '20px' }}>
          <h4 style={{ fontSize: '14px', fontWeight: 700, color: 'var(--color-ink)', textTransform: 'uppercase', marginBottom: '14px' }}>
            Claims for Review ({claims.length})
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {claims.map((c) => {
              const isSelected = c.claim_id === activeClaimId;
              return (
                <div
                  key={c.id}
                  onClick={() => {
                    setActiveClaimId(c.claim_id);
                    setIsEditing(false);
                    setNotes('');
                  }}
                  style={{
                    padding: '12px 14px',
                    borderRadius: 'var(--radius-md)',
                    background: isSelected ? 'var(--color-cream)' : 'transparent',
                    border: `1px solid ${isSelected ? 'var(--color-rust)' : 'transparent'}`,
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ fontFamily: 'monospace', fontWeight: 700, fontSize: '12px', color: 'var(--color-ink)' }}>
                      {c.claim_id}
                    </span>
                    <span className={`badge-tag ${
                      c.verification_status === 'approved' ? 'badge-approved' :
                      c.verification_status === 'flagged' ? 'badge-flagged' :
                      c.verification_status === 'edited' ? 'badge-edited' : 'badge-pending'
                    }`} style={{ fontSize: '10px', padding: '2px 6px' }}>
                      {c.verification_status}
                    </span>
                  </div>
                  <div style={{
                    fontSize: '13px',
                    color: 'var(--color-ink)',
                    lineHeight: 1.35,
                    overflow: 'hidden',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical'
                  }}>
                    {c.claim_text}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Active Claim Medical Evaluation Card */}
        {currentClaim ? (
          <div className="steer-card" style={{ padding: '32px' }}>
            {/* Header info */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{
                  fontFamily: 'monospace',
                  fontSize: '15px',
                  fontWeight: 700,
                  background: 'var(--color-cream)',
                  padding: '4px 10px',
                  borderRadius: '6px'
                }}>
                  {currentClaim.claim_id}
                </span>

                <span className={`badge-tag ${
                  currentClaim.verification_status === 'approved' ? 'badge-approved' :
                  currentClaim.verification_status === 'flagged' ? 'badge-flagged' :
                  currentClaim.verification_status === 'edited' ? 'badge-edited' : 'badge-pending'
                }`}>
                  {currentClaim.verification_status.toUpperCase()}
                </span>

                <span className="badge-tag badge-blush">
                  {currentClaim.support_level.toUpperCase()} EVIDENCE
                </span>
              </div>

              {currentClaim.confidence_estimate && (
                <div style={{ fontSize: '13px', color: 'var(--color-ink-muted)' }}>
                  AI Confidence Estimate: <strong>{Math.round(currentClaim.confidence_estimate * 100)}%</strong>
                </div>
              )}
            </div>

            {/* Extracted Claim Text / Edit Mode */}
            <div style={{ marginBottom: '24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <label style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>
                  Target Clinical Claim
                </label>
                {!isEditing && (
                  <button
                    onClick={startEdit}
                    className="btn-secondary"
                    style={{ fontSize: '12px', padding: '4px 10px' }}
                  >
                    <Edit3 size={13} />
                    <span>Edit Wording</span>
                  </button>
                )}
              </div>

              {isEditing ? (
                <div>
                  <textarea
                    rows={4}
                    value={editedText}
                    onChange={(e) => setEditedText(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '14px',
                      borderRadius: 'var(--radius-md)',
                      border: '2px solid var(--color-rust)',
                      fontFamily: 'var(--font-sans)',
                      fontSize: '15px',
                      color: 'var(--color-ink)',
                      marginBottom: '10px'
                    }}
                  />
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                      onClick={() => handleAction('edit')}
                      disabled={isSubmitting}
                      className="btn-primary"
                      style={{ fontSize: '13px', padding: '8px 16px' }}
                    >
                      <Save size={14} />
                      <span>Save Edited Claim</span>
                    </button>
                    <button
                      onClick={() => setIsEditing(false)}
                      className="btn-secondary"
                      style={{ fontSize: '13px', padding: '8px 16px' }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div style={{
                  fontSize: '18px',
                  fontWeight: 600,
                  color: 'var(--color-ink)',
                  lineHeight: 1.45,
                  padding: '14px 18px',
                  background: 'var(--color-cream)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--color-card-border)'
                }}>
                  {currentClaim.claim_text}
                </div>
              )}

              {currentClaim.original_claim_text && (
                <div style={{ fontSize: '12px', color: 'var(--color-clay)', marginTop: '6px', fontStyle: 'italic' }}>
                  Original AI extraction preserved: "{currentClaim.original_claim_text}"
                </div>
              )}
            </div>

            {/* Verbatim Supporting Passage Quote */}
            <div style={{
              background: '#FFF9F4',
              border: '1px solid var(--color-blush)',
              borderRadius: 'var(--radius-md)',
              padding: '20px 24px',
              marginBottom: '24px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <Quote size={18} color="var(--color-rust)" />
                <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-rust)', textTransform: 'uppercase' }}>
                  Exact Verbatim Passage From Paper
                </span>
                {currentClaim.page_number && (
                  <span style={{ fontSize: '12px', color: 'var(--color-clay)', marginLeft: 'auto' }}>
                    Cited Location: Page {currentClaim.page_number} ({currentClaim.section || 'Results'})
                  </span>
                )}
              </div>
              <div style={{ fontSize: '15px', fontStyle: 'italic', color: 'var(--color-ink)', lineHeight: 1.6 }}>
                "{currentClaim.evidence_quote}"
              </div>
              {currentClaim.support_notes && (
                <div style={{ fontSize: '12px', color: 'var(--color-clay)', marginTop: '8px' }}>
                  Cross-Examination: {currentClaim.support_notes}
                </div>
              )}
            </div>

            {/* Context & Limitations */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '16px',
              background: 'var(--color-cream)',
              padding: '16px 20px',
              borderRadius: 'var(--radius-md)',
              marginBottom: '28px',
              fontSize: '13px'
            }}>
              <div>
                <span style={{ color: 'var(--color-clay)', fontWeight: 600 }}>Study Design:</span>{' '}
                <strong>{currentClaim.evidence_type}</strong>
              </div>
              <div>
                <span style={{ color: 'var(--color-clay)', fontWeight: 600 }}>Cohort:</span>{' '}
                <strong>{currentClaim.population || 'Adult subjects'}</strong>
              </div>
              {currentClaim.limitations && currentClaim.limitations.length > 0 && (
                <div style={{ gridColumn: 'span 2' }}>
                  <span style={{ color: 'var(--color-clay)', fontWeight: 600 }}>Study Limitation:</span>{' '}
                  <span>{currentClaim.limitations[0]}</span>
                </div>
              )}
            </div>

            {/* Reviewer Decision Actions Box */}
            <div style={{
              background: 'var(--color-soft-paper)',
              border: '2px solid var(--color-blush)',
              borderRadius: 'var(--radius-lg)',
              padding: '24px'
            }}>
              <h4 style={{ fontSize: '16px', color: 'var(--color-ink)', marginBottom: '12px' }}>
                Record Physician Decision
              </h4>

              <div style={{ marginBottom: '18px' }}>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--color-ink-muted)', marginBottom: '6px' }}>
                  Clinical Reviewer Notes & Modifications Rationale (Optional)
                </label>
                <input
                  type="text"
                  placeholder="e.g. Verified with Continuous Glucose Monitoring chart on Page 3; confirmed non-insulin pathway."
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--color-clay)',
                    background: 'var(--color-white)',
                    fontSize: '13px',
                    fontFamily: 'var(--font-sans)',
                    color: 'var(--color-ink)'
                  }}
                />
              </div>

              {/* Action Buttons */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
                <button
                  onClick={() => handleAction('approve')}
                  disabled={isSubmitting}
                  className="btn-primary"
                  style={{ background: '#2E7D32', borderColor: '#1B5E20' }}
                >
                  <CheckCircle size={16} />
                  <span>Approve Claim</span>
                </button>

                <button
                  onClick={() => handleAction('flag')}
                  disabled={isSubmitting}
                  className="btn-secondary"
                  style={{ color: '#E65100', borderColor: '#FFE082', background: '#FFF8E1' }}
                >
                  <AlertTriangle size={16} />
                  <span>Flag for Verification</span>
                </button>

                <button
                  onClick={() => handleAction('reject')}
                  disabled={isSubmitting}
                  className="btn-secondary"
                  style={{ color: '#C62828', borderColor: '#EF9A9A', background: '#FFEBEE' }}
                >
                  <XCircle size={16} />
                  <span>Reject Claim</span>
                </button>
              </div>

              {currentClaim.reviewed_at && (
                <div style={{
                  fontSize: '12px',
                  color: 'var(--color-clay)',
                  marginTop: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}>
                  <Clock size={13} />
                  <span>
                    Last reviewed by {currentClaim.reviewed_by || 'Reviewer'} on{' '}
                    {new Date(currentClaim.reviewed_at).toLocaleString()}
                  </span>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="steer-card" style={{ padding: '40px', textAlign: 'center' }}>
            No claims available for review.
          </div>
        )}
      </div>
    </div>
  );
};
