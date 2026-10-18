import React, { useState, useRef } from 'react';
import { X, Upload, Globe, FileText, Sparkles, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

interface NewProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onProjectCreated: (projectId: string) => void;
  onLoadSamplePaper: () => void;
}

export const NewProjectModal: React.FC<NewProjectModalProps> = ({
  isOpen,
  onClose,
  onProjectCreated,
  onLoadSamplePaper,
}) => {
  const [activeTab, setActiveTab] = useState<'pdf' | 'url'>('pdf');
  const [title, setTitle] = useState('');
  const [campaignTopic, setCampaignTopic] = useState('');
  const [url, setUrl] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const resetForm = () => {
    setTitle('');
    setCampaignTopic('');
    setUrl('');
    setFile(null);
    setErrorMessage(null);
    setIsLoading(false);
  };

  React.useEffect(() => {
    if (isOpen) {
      resetForm();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleFileChange = (selectedFile: File) => {
    setErrorMessage(null);
    if (!selectedFile.name.toLowerCase().endsWith('.pdf')) {
      setErrorMessage('Only PDF scientific research papers are supported.');
      return;
    }
    if (selectedFile.size > 50 * 1024 * 1024) {
      setErrorMessage('File size exceeds 50MB limit.');
      return;
    }
    setFile(selectedFile);
    // Auto populate clean title from filename for the new document
    const clean = selectedFile.name.replace(/\.pdf$/i, '').replace(/[_-]/g, ' ');
    setTitle(clean.charAt(0).toUpperCase() + clean.slice(1));
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!title.trim()) {
      setErrorMessage('Please enter a project title.');
      return;
    }

    if (activeTab === 'pdf' && !file) {
      setErrorMessage('Please upload a PDF file of the scientific research paper.');
      return;
    }

    if (activeTab === 'url' && !url.trim()) {
      setErrorMessage('Please provide a valid research paper URL.');
      return;
    }

    try {
      setIsLoading(true);

      // 1. Create project
      const proj = await api.createProject({
        title: title.trim(),
        campaign_topic: campaignTopic.trim() || undefined,
        source_type: activeTab,
        source_url: activeTab === 'url' ? url.trim() : undefined,
      });

      // 2. If PDF, upload file
      if (activeTab === 'pdf' && file) {
        await api.uploadPdf(proj.id, file);
      }

      // 3. Trigger processing pipeline
      await api.processPipeline(proj.id);

      setIsLoading(false);
      resetForm();
      onClose();
      onProjectCreated(proj.id);
    } catch (err: any) {
      setIsLoading(false);
      setErrorMessage(err.message || 'Failed to process scientific paper. Please check the file or URL.');
    }
  };

  return (
    <div className="modal-overlay" onClick={() => { resetForm(); onClose(); }}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ padding: '36px' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
          <div>
            <div className="badge-tag badge-blush" style={{ marginBottom: '8px' }}>
              NEW RESEARCH INGESTION
            </div>
            <h2 style={{ fontSize: '26px', color: 'var(--color-ink)' }}>Add Research Paper</h2>
          </div>
          <button 
            onClick={() => { resetForm(); onClose(); }} 
            disabled={isLoading}
            style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--color-clay)' }}
          >
            <X size={24} />
          </button>
        </div>

        {/* Quick Sample Paper Loader Banner */}
        <div style={{
          background: 'var(--color-rust-light)',
          border: '1px solid var(--color-blush)',
          borderRadius: 'var(--radius-md)',
          padding: '16px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '24px',
          gap: '16px'
        }}>
          <div>
            <div style={{ fontWeight: 700, fontSize: '14px', color: 'var(--color-rust)' }}>
              Want to test immediately without uploading?
            </div>
            <div style={{ fontSize: '13px', color: 'var(--color-ink-muted)' }}>
              Load our verified clinical study on postprandial walking & glucose control in Indian adults.
            </div>
          </div>
          <button
            type="button"
            onClick={() => {
              onClose();
              onLoadSamplePaper();
            }}
            disabled={isLoading}
            className="btn-primary"
            style={{ whiteSpace: 'nowrap', padding: '8px 16px', fontSize: '13px' }}
          >
            <Sparkles size={15} />
            <span>Load Sample Study</span>
          </button>
        </div>

        {/* Tab switch */}
        <div style={{
          display: 'flex',
          background: 'var(--color-cream)',
          padding: '4px',
          borderRadius: 'var(--radius-md)',
          marginBottom: '24px'
        }}>
          <button
            type="button"
            className={`steer-tab-btn ${activeTab === 'pdf' ? 'active' : ''}`}
            onClick={() => setActiveTab('pdf')}
            style={{ flex: 1, justifyContent: 'center' }}
          >
            <FileText size={16} />
            <span>Upload Research PDF</span>
          </button>
          <button
            type="button"
            className={`steer-tab-btn ${activeTab === 'url' ? 'active' : ''}`}
            onClick={() => setActiveTab('url')}
            style={{ flex: 1, justifyContent: 'center' }}
          >
            <Globe size={16} />
            <span>Public Paper URL</span>
          </button>
        </div>

        {errorMessage && (
          <div style={{
            background: '#FFEBEE',
            border: '1px solid #EF9A9A',
            color: '#C62828',
            borderRadius: 'var(--radius-md)',
            padding: '12px 16px',
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '10px',
            fontSize: '13px'
          }}>
            <AlertCircle size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>{errorMessage}</div>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Metadata inputs */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: 'var(--color-ink)', marginBottom: '8px' }}>
              Project Title *
            </label>
            <input
              type="text"
              placeholder="e.g. Postprandial Glucose & 10-Minute Walk Study"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isLoading}
              style={{
                width: '100%',
                padding: '12px 16px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-clay)',
                background: 'var(--color-white)',
                fontFamily: 'var(--font-sans)',
                fontSize: '14px',
                color: 'var(--color-ink)'
              }}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: 'var(--color-ink)', marginBottom: '8px' }}>
              Campaign Topic or Focus (Optional)
            </label>
            <input
              type="text"
              placeholder="e.g. Shatapadi Habit / Preventing Evening Energy Crashes"
              value={campaignTopic}
              onChange={(e) => setCampaignTopic(e.target.value)}
              disabled={isLoading}
              style={{
                width: '100%',
                padding: '12px 16px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-clay)',
                background: 'var(--color-white)',
                fontFamily: 'var(--font-sans)',
                fontSize: '14px',
                color: 'var(--color-ink)'
              }}
            />
          </div>

          {/* PDF Drag & Drop */}
          {activeTab === 'pdf' ? (
            <div style={{ marginBottom: '28px' }}>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                style={{ display: 'none' }}
                onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
              />
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                style={{
                  border: `2px dashed ${isDragging ? 'var(--color-rust)' : file ? 'var(--color-clay)' : 'var(--color-blush)'}`,
                  background: isDragging ? 'var(--color-rust-light)' : 'var(--color-cream)',
                  borderRadius: 'var(--radius-lg)',
                  padding: '36px 20px',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                <div style={{
                  width: '52px',
                  height: '52px',
                  borderRadius: '50%',
                  background: 'var(--color-soft-paper)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 14px'
                }}>
                  <Upload size={22} color="var(--color-rust)" />
                </div>

                {file ? (
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '15px', color: 'var(--color-ink)', marginBottom: '4px' }}>
                      {file.name}
                    </div>
                    <div style={{ fontSize: '12px', color: 'var(--color-clay)' }}>
                      {(file.size / (1024 * 1024)).toFixed(2)} MB • Click or drag to replace
                    </div>
                  </div>
                ) : (
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '15px', color: 'var(--color-ink)', marginBottom: '4px' }}>
                      Drag and drop your paper PDF here
                    </div>
                    <div style={{ fontSize: '13px', color: 'var(--color-ink-muted)' }}>
                      Or click to browse from your computer (up to 50MB)
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            /* URL Input */
            <div style={{ marginBottom: '28px' }}>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: 'var(--color-ink)', marginBottom: '8px' }}>
                Open-Access Paper or Preprint URL
              </label>
              <input
                type="url"
                placeholder="https://pmc.ncbi.nlm.nih.gov/articles/PMC..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                disabled={isLoading}
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--color-clay)',
                  background: 'var(--color-white)',
                  fontFamily: 'var(--font-sans)',
                  fontSize: '14px',
                  color: 'var(--color-ink)'
                }}
              />
              <div style={{ fontSize: '12px', color: 'var(--color-clay)', marginTop: '8px' }}>
                Note: Only publicly accessible open-access papers are supported. If behind a paywall, please download the PDF and upload it directly.
              </div>
            </div>
          )}

          {/* Action buttons */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '12px' }}>
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary"
              style={{ minWidth: '180px', justifyContent: 'center' }}
            >
              {isLoading ? (
                <span>Ingesting & Processing...</span>
              ) : (
                <span>Ingest & Start Studio</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
