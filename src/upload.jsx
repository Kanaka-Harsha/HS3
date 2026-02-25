import { useState } from 'react';
import './upload.css';

function Upload({ onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState({ message: '', color: '' });
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
      setStatus({ message: '', color: '' });
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setStatus({ message: "Please select a file first", color: "var(--danger)" });
      return;
    }

    setIsUploading(true);
    setStatus({ message: "Preparing upload...", color: "var(--primary)" });

    try {
      const lambdaResponse = await fetch('https://hbriggwyii.execute-api.us-east-1.amazonaws.com/hs3API/s3Uploader', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filename: selectedFile.name,
          content_type: selectedFile.type,
          file_size: (selectedFile.size / (1024 * 1024)).toFixed(2)
        }),
      });

      if (!lambdaResponse.ok) {
        throw new Error("Failed to get upload URL");
      }

      const { upload_url } = await lambdaResponse.json();

      setStatus({ message: "Uploading your file...", color: "var(--primary)" });

      const s3Response = await fetch(upload_url, {
        method: 'PUT',
        body: selectedFile,
        headers: {
          'Content-Type': selectedFile.type,
        },
      });

      if (s3Response.ok) {
        setStatus({ message: "Successfully uploaded!", color: "var(--success)" });
        setSelectedFile(null);
        if (onUploadSuccess) {
          onUploadSuccess();
        }
      } else {
        setStatus({ message: "Upload failed", color: "var(--danger)" });
      }
    } catch (error) {
      console.error("Upload error:", error);
      setStatus({ message: "Error: " + error.message, color: "var(--danger)" });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-card">
      <div className="upload-header">
        <h1>Upload New Files</h1>
        <p className="subtitle">Securely add files to your HS3 Drive</p>
      </div>
      
      <div className="drop-zone">
        <label className="select-file-label">
          {selectedFile ? 'Change File' : 'Select File'}
          <input 
            type="file" 
            className="file-input" 
            onChange={handleFileChange}
          />
        </label>
        
        {selectedFile ? (
          <span className="selected-file-name">{selectedFile.name}</span>
        ) : (
          <span className="subtitle">or drag and drop here</span>
        )}
      </div>

      <button 
        className="upload-btn" 
        onClick={handleUpload}
        disabled={!selectedFile || isUploading}
      >
        {isUploading ? 'Uploading...' : 'Upload to Drive'}
      </button>

      {status.message && (
        <p className="upload-status" style={{ color: status.color }}>
          {status.message}
        </p>
      )}
    </div>
  );
}

export default Upload;