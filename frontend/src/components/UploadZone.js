import React from 'react';
import { useDropzone } from 'react-dropzone';
import './UploadZone.css';

function UploadZone({ file, onFileSelect }) {
  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: 5 * 1024 * 1024, // 5MB
    multiple: false,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    },
  });

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  // File selected state
  if (file) {
    return (
      <div className="upload-zone upload-zone--filled">
        <div className="upload-file-info">
          <div className="upload-file-icon">📄</div>
          <div className="upload-file-details">
            <div className="upload-file-name">{file.name}</div>
            <div className="upload-file-size">{formatSize(file.size)}</div>
          </div>
          <button
            type="button"
            className="upload-remove-btn"
            onClick={(e) => {
              e.stopPropagation();
              onFileSelect(null);
            }}
            aria-label="Remove file"
          >
            ✕
          </button>
        </div>
      </div>
    );
  }

  // Empty / drag state
  return (
    <div
      {...getRootProps()}
      className={`upload-zone ${isDragActive ? 'upload-zone--active' : ''} ${
        isDragReject ? 'upload-zone--reject' : ''
      }`}
    >
      <input {...getInputProps()} />
      <div className="upload-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
      </div>
      <div className="upload-text-primary">
        {isDragActive ? 'Drop your resume here' : 'Drag your resume here or click to browse'}
      </div>
      <div className="upload-text-secondary">
        PDF or DOCX · Max 5MB
      </div>
    </div>
  );
}

export default UploadZone;