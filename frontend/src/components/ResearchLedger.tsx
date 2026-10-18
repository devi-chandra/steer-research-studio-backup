import React, { useState } from 'react';
import { 
  FileText, 
  ExternalLink, 
  Quote, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldAlert, 
  Filter, 
  Search,
  BookOpen,
  ArrowRight
} from 'lucide-react';
import { Project, Claim } from '../types';

interface ResearchLedgerProps {
  project: Project;
  onOpenReview: (claimId: string) => void;
  onOpenPassage: (claim: Claim) => void;
}

export const ResearchLedger: React.FC<ResearchLedgerProps> = ({
  project,
  onOpenReview,
  onOpenPassage,
}) => {
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const meta = project.paper_metadata || {};
  const claims = project.claims || [];

  const filteredClaims = claims.filter((c) => {
    const matchesStatus = statusFilter === 'all' || c.verification_status === statusFilter;
    const matchesSearch = 
      c.claim_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.evidence_quote.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.claim_id.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Paper Provenance & Study Overview Card */}
      <div className="steer-card" style={{ padding: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '20px', marginBottom: '18px' }}>
          <div>
            <div className="badge-tag badge-blush" style={{ marginBottom: '10px' }}>
              SCIENTIFIC PAPER PROVENANCE
            </div>
            <h2 style={{ fontSize: '26px', color: 'var(--color-ink)', lineHeight: 1.25 }}>
              {meta.title || project.title}
            </h2>
          </div>

          {meta.doi && (
            <a
              href={`https://doi.org/${meta.doi}`}
              target="_blank"
              rel="noreferrer"
              className="btn-secondary"
              style={{ fontSize: '12px', padding: '6px 14px', flexShrink: 0 }}
            >
              <span>DOI: {meta.doi}</span>
              <ExternalLink size={14} />
            </a>
          )}
        </div>

        {/* Paper Details Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          background: 'var(--color-cream)',
          padding: '18px 22px',
          borderRadius: 'var(--radius-md)',
          marginBottom: '22px'
        }}>
          <div>
            <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>Authors</div>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-ink)', marginTop: '2px' }}>
              {meta.authors && meta.authors.length > 0 ? meta.authors.join(', ') : 'Authors in Paper'}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>Publication Year</div>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-ink)', marginTop: '2px' }}>
              {meta.year || '2024'}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>Research Design</div>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-rust)', marginTop: '2px' }}>
              {meta.study_type || 'Randomized Crossover Clinical Trial'}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase' }}>Page Count</div>
            <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-ink)', marginTop: '2px' }}>
              {meta.pages_analyzed && meta.page_count && meta.pages_analyzed < meta.page_count
                ? `${meta.pages_analyzed} of ${meta.page_count} Pages Analyzed`
                : `${meta.page_count || 5} Pages Analyzed`}
            </div>
          </div>
        </div>

        {/* Abstract */}
        {meta.abstract && (
          <div style={{ marginBottom: '22px' }}>
            <h4 style={{ fontSize: '14px', fontWeight: 700, color: 'var(--color-ink)', textTransform: 'uppercase', marginBottom: '8px' }}>
              Clinical Abstract
            </h4>
            <p style={{ fontSize: '14px', color: 'var(--color-ink-muted)', lineHeight: 1.65 }}>
              {meta.abstract}
            </p>
          </div>
        )}

        {/* Key Findings and Limitations Side by Side */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div style={{ background: '#F4F9F4', border: '1px solid #C8E6C9', borderRadius: 'var(--radius-md)', padding: '18px 20px' }}>
            <div style={{ fontWeight: 700, fontSize: '13px', color: '#2E7D32', textTransform: 'uppercase', marginBottom: '10px' }}>
              Key Clinical Discoveries
            </div>
            <ul style={{ paddingLeft: '18px', fontSize: '13px', color: 'var(--color-ink)', lineHeight: 1.6 }}>
              {meta.key_findings && meta.key_findings.length > 0 ? (
                meta.key_findings.map((f: string, idx: number) => <li key={idx}>{f}</li>)
              ) : (
                <li style={{ color: 'var(--color-ink-muted)', fontStyle: 'italic' }}>No specific clinical discoveries extracted yet for this paper.</li>
              )}
            </ul>
          </div>

          <div style={{ background: '#FFF8E1', border: '1px solid #FFE082', borderRadius: 'var(--radius-md)', padding: '18px 20px' }}>
            <div style={{ fontWeight: 700, fontSize: '13px', color: '#E65100', textTransform: 'uppercase', marginBottom: '10px' }}>
              Study Limitations & Context
            </div>
            <ul style={{ paddingLeft: '18px', fontSize: '13px', color: 'var(--color-ink)', lineHeight: 1.6 }}>
              {meta.limitations && meta.limitations.length > 0 ? (
                meta.limitations.map((l: string, idx: number) => <li key={idx}>{l}</li>)
              ) : (
                <li style={{ color: 'var(--color-ink-muted)', fontStyle: 'italic' }}>No specific study limitations recorded for this document.</li>
              )}
            </ul>
          </div>
        </div>
      </div>

      {/* Claims Ledger Header & Filter Controls */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '14px' }}>
          <div>
            <h2 style={{ fontSize: '24px', color: 'var(--color-ink)' }}>Source-Traceable Claims Ledger</h2>
            <p style={{ fontSize: '14px', color: 'var(--color-ink-muted)' }}>
              Every extracted health statement is linked to an exact verbatim passage in the paper
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {/* Search Input */}
            <div style={{ position: 'relative' }}>
              <Search size={16} color="var(--color-clay)" style={{ position: 'absolute', left: '12px', top: '10px' }} />
              <input
                type="text"
                placeholder="Search claims & quotes..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{
                  padding: '8px 14px 8px 36px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--color-clay)',
                  background: 'var(--color-white)',
                  fontSize: '13px',
                  fontFamily: 'var(--font-sans)',
                  color: 'var(--color-ink)'
                }}
              />
            </div>

            {/* Filter Buttons */}
            <div style={{ display: 'flex', background: 'var(--color-cream)', padding: '3px', borderRadius: 'var(--radius-md)' }}>
              {['all', 'pending', 'approved', 'flagged', 'edited'].map((st) => (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: 'var(--radius-sm)',
                    border: 'none',
                    background: statusFilter === st ? 'var(--color-rust)' : 'transparent',
                    color: statusFilter === st ? '#FFFFFF' : 'var(--color-ink-muted)',
                    fontSize: '12px',
                    fontWeight: 600,
                    cursor: 'pointer',
                    textTransform: 'capitalize'
                  }}
                >
                  {st}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Claims List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {filteredClaims.length === 0 ? (
            <div className="steer-card" style={{ padding: '40px', textAlign: 'center', color: 'var(--color-ink-muted)' }}>
              No claims found matching your filter criteria.
            </div>
          ) : (
            filteredClaims.map((claim) => (
              <div 
                key={claim.id} 
                className="steer-card"
                style={{
                  padding: '24px 28px',
                  borderLeft: `4px solid ${
                    claim.verification_status === 'approved' ? '#4CAF50' :
                    claim.verification_status === 'flagged' ? '#FF5722' :
                    claim.verification_status === 'edited' ? '#0288D1' : 'var(--color-clay)'
                  }`
                }}
              >
                {/* Claim Top Bar */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{
                      fontFamily: 'monospace',
                      fontWeight: 700,
                      fontSize: '13px',
                      background: 'var(--color-cream)',
                      padding: '4px 8px',
                      borderRadius: '6px',
                      color: 'var(--color-ink)'
                    }}>
                      {claim.claim_id}
                    </span>

                    <span className={`badge-tag ${
                      claim.verification_status === 'approved' ? 'badge-approved' :
                      claim.verification_status === 'flagged' ? 'badge-flagged' :
                      claim.verification_status === 'edited' ? 'badge-edited' : 'badge-pending'
                    }`}>
                      {claim.verification_status.toUpperCase()}
                    </span>

                    <span className={`badge-tag ${
                      claim.support_level === 'strong' ? 'badge-approved' :
                      claim.support_level === 'moderate' ? 'badge-blush' : 'badge-flagged'
                    }`}>
                      {claim.support_level.toUpperCase()} SUPPORT
                    </span>

                    {claim.page_number && (
                      <span style={{ fontSize: '12px', color: 'var(--color-clay)', fontWeight: 600 }}>
                        Page {claim.page_number} • Section: {claim.section || 'Results'}
                      </span>
                    )}
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {claim.confidence_estimate && (
                      <span style={{ fontSize: '12px', color: 'var(--color-ink-muted)' }}>
                        AI Confidence Estimate: <strong>{Math.round(claim.confidence_estimate * 100)}%</strong>
                      </span>
                    )}
                    <button
                      onClick={() => onOpenReview(claim.claim_id)}
                      className="btn-primary"
                      style={{ padding: '6px 14px', fontSize: '12px' }}
                    >
                      <span>Medical Review</span>
                      <ArrowRight size={13} />
                    </button>
                  </div>
                </div>

                {/* Claim Wording */}
                <div style={{ marginBottom: '16px' }}>
                  <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-clay)', textTransform: 'uppercase', marginBottom: '4px' }}>
                    Extracted Factual Claim
                  </div>
                  <div style={{ fontSize: '16px', fontWeight: 600, color: 'var(--color-ink)', lineHeight: 1.4 }}>
                    {claim.claim_text}
                  </div>
                  {claim.original_claim_text && (
                    <div style={{ fontSize: '12px', color: 'var(--color-clay)', marginTop: '4px', fontStyle: 'italic' }}>
                      Original text: "{claim.original_claim_text}"
                    </div>
                  )}
                </div>

                {/* Exact Supporting Passage Quote Card */}
                <div style={{
                  background: 'var(--color-cream)',
                  border: '1px solid var(--color-blush)',
                  borderRadius: 'var(--radius-md)',
                  padding: '16px 20px',
                  marginBottom: '16px',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '12px'
                }}>
                  <Quote size={22} color="var(--color-rust)" style={{ flexShrink: 0, marginTop: '2px' }} />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-rust)', textTransform: 'uppercase', marginBottom: '2px' }}>
                      Exact Verbatim Evidence Passage
                    </div>
                    <div style={{ fontSize: '14px', fontStyle: 'italic', color: 'var(--color-ink)', lineHeight: 1.5 }}>
                      "{claim.evidence_quote}"
                    </div>
                    {claim.support_notes && (
                      <div style={{ fontSize: '12px', color: 'var(--color-clay)', marginTop: '6px' }}>
                        ✓ {claim.support_notes}
                      </div>
                    )}
                  </div>
                </div>

                {/* Evidence Context & Meta */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  fontSize: '12px',
                  color: 'var(--color-ink-muted)',
                  borderTop: '1px solid var(--color-card-border)',
                  paddingTop: '12px'
                }}>
                  <div style={{ display: 'flex', gap: '20px' }}>
                    <span>Study Type: <strong>{claim.evidence_type}</strong></span>
                    {claim.population && <span>Cohort: <strong>{claim.population}</strong></span>}
                    {claim.sample_size && <span>Sample: <strong>{claim.sample_size}</strong></span>}
                  </div>

                  {claim.reviewer_notes && (
                    <div style={{ color: 'var(--color-maroon)', fontWeight: 600 }}>
                      Doctor Note: "{claim.reviewer_notes}"
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
