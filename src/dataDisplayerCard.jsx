import './dataDisplayerCard.css'

function DataDisplayerCard({ file, onDelete }) {
  const formatFileSize = (bytes) => {
    if (!bytes || bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
  }

  const formatFileType = (contentType, filename) => {
    if (filename && filename.includes('.')) {
      const ext = filename.split('.').pop().toLowerCase()
      if (ext === 'jpeg') return 'jpg'
      if (ext === 'docx') return 'docs'
      return ext
    }
    if (!contentType) return 'Unknown'
    const mimeMap = {
      'image/jpeg': 'jpg',
      'image/png': 'png',
      'application/pdf': 'pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docs',
      'application/msword': 'doc',
      'application/xml': 'xml',
      'text/csv': 'csv',
      'video/mp4': 'mp4',
      'audio/mpeg': 'mp3',
      'text/plain': 'txt',
      'application/zip': 'zip'
    }
    if (mimeMap[contentType]) return mimeMap[contentType]
    const parts = contentType.split('/')
    if (parts.length > 1) {
      let subtype = parts[1].split('+')[0]
      if (subtype.startsWith('vnd.')) subtype = subtype.split('.').pop()
      return subtype
    }
    return 'file'
  }

  const downloadFile = () => {
    if (file.access_url) {
      window.open(file.access_url, '_blank')
    } else {
      alert('Download URL not available')
    }
  }

  return (
    <div className="file-card">
      <div className="file-info">
        <h3 className="file-name" title={file.filename}>{file.filename || "Unknown File"}</h3>
        <div className="file-details">
          <span className="file-type-badge">{formatFileType(file.content_type, file.filename)}</span>
          <span className="file-size">{formatFileSize(file.file_size)}</span>
        </div>
      </div>
      <div className="file-actions">
        <button className="action-btn btn-download" onClick={downloadFile}>
          Download
        </button>
        <button className="action-btn btn-delete" onClick={() => onDelete(file.filename)}>
          Delete
        </button>
      </div>
    </div>
  )
}

export default DataDisplayerCard