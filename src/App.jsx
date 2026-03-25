import { useState, useEffect } from 'react'
import Upload from './upload'
import Login from './login'
import NavBar from './navbar'
import DataDisplayerCard from './dataDisplayerCard'
import './App.css'

function App() {

  const [isLoggedin, setIsLoggedIn] = useState(() => {
    return localStorage.getItem("isLoggedin") === "true";
  });

  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const fetchFiles = async (delay = 0) => {
    if (!isLoggedin) return;
    
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
    }

    setLoading(true);
    try {
      const response = await fetch('YOUR API KEY');
      if (response.ok) {
        const data = await response.json();
        setFiles(Array.isArray(data) ? data : (data.files || []));
      } else {
        const errorText = await response.text();
        console.error(`Failed to fetch files. Status: ${response.status}. Error: ${errorText}`);
      }
    } catch (error) {
      console.error("Network error fetching files:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isLoggedin) {
      fetchFiles();
    }
  }, [isLoggedin]);

  const handleLogin = () => {
    localStorage.setItem("isLoggedin", "true");
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("isLoggedin");
    setIsLoggedIn(false);
    setFiles([]);
  };

  const handleDeleteFile = async (filename) => {
    if (window.confirm(`Are you sure you want to delete ${filename}?`)) {
      try {
        const lambdaResponse = await fetch('YOUR API KEY', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    filename: filename,
                }),
            });
        if (lambdaResponse.ok) {
            alert("Successfully deleted " + filename);
            fetchFiles(2000);
        } else {
            const errorText = await lambdaResponse.text();
            let errorMessage = "Unknown error";
            try {
                const errorData = JSON.parse(errorText);
                errorMessage = errorData.message || errorData.body || errorText;
            } catch (e) {
                errorMessage = errorText || "Unknown error";
            }
            console.error("Delete failed:", errorMessage);
            alert("Failed to delete file: " + errorMessage);
        }
      } catch (error) {
        console.error("Error deleting file:", error);
      }
    }
  };

  const calculateTotalStorage = () => {
    return files.reduce((acc, file) => acc + (file.file_size || 0), 0);
  };

  const totalStorage = calculateTotalStorage();
  const STORAGE_LIMIT = 10 * 1024 * 1024 * 1024; // 10 GB
  const storagePercentage = Math.min((totalStorage / STORAGE_LIMIT) * 100, 100);

  const formatStorageSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div id="root">
      <NavBar isLoggedin={isLoggedin} onLogout={handleLogout} />
      
      {isLoggedin ? (
        <div className="app-container">
          <div className="dashboard">
            <section className="upload-section-redesigned">
              <Upload onUploadSuccess={() => fetchFiles(3000)} />
            </section>

            <section className="storage-section">
              <div className="storage-header-container">
                <h2 className="section-title">My Storage</h2>
                <div className="storage-progress-wrapper">
                  <div className="storage-progress-info">
                    <span>{formatStorageSize(totalStorage)} / 10 GB Used</span>
                    <span>{storagePercentage.toFixed(1)}%</span>
                  </div>
                  <div className="progress-bar-container">
                    <div 
                      className={`progress-bar-fill ${storagePercentage > 90 ? 'danger' : storagePercentage > 75 ? 'warning' : ''}`}
                      style={{ width: `${storagePercentage}%` }}
                    ></div>
                  </div>
                </div>
              </div>
              {loading ? (
                <div className="loading-state">Loading your files...</div>
              ) : (
                <div className="file-grid">
                  {files.length > 0 ? (
                    files.map((file, index) => (
                      <DataDisplayerCard 
                        key={index} 
                        file={file} 
                        onDelete={handleDeleteFile} 
                      />
                    ))
                  ) : (
                    <div className="empty-state">
                      <p>No files found in your drive.</p>
                      <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>Upload something to get started!</p>
                    </div>
                  )}
                </div>
              )}
            </section>
          </div>
        </div>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  )
}

export default App
