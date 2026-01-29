import { useState } from 'react';

function Upload()
{
    /* 
    // OLD CODE - COMMENTED AS REQUESTED
    const uploadFile = () =>
    {
        const inputFile=document.getElementByClassName("fileInput");
        const status=document.getElementByclassName("status");

        if(!inputFile.files.length)
        {
            status.innertext="Please Select A File";
            status.style.color="red";
            return;
        }
        else
        {
            status.innerText="File Uploaded Successfully";
            status.style.color="green";
        }
    }
    */

    const [selectedFile, setSelectedFile] = useState(null);
    const [status, setStatus] = useState({ message: '', color: '' });

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            setSelectedFile(e.target.files[0]);
            setStatus({ message: '', color: '' });
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setStatus({ message: "Please Select A File", color: "red" });
            return;
        }

        try {
            setStatus({ message: "Requesting upload URL...", color: "blue" });
            
            const lambdaResponse = await fetch('https://2wb91iw6gk.execute-api.us-east-1.amazonaws.com/s3uploader', {
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
                const errorData = await lambdaResponse.json();
                console.error("Lambda Error:", errorData);
                throw new Error("Failed to get upload URL");
            }

            const { upload_url } = await lambdaResponse.json();

            // 2. Upload the file to S3 using the pre-signed URL
            setStatus({ message: "Uploading to S3...", color: "blue" });

            const s3Response = await fetch(upload_url, {
                method: 'PUT',
                body: selectedFile,
                headers: {
                    'Content-Type': selectedFile.type, // Important: Must match what was sent to Lambda
                },
            });

            if (s3Response.ok) {
                setStatus({ message: "File Uploaded Successfully", color: "green" });
            } else {
                console.error("S3 Upload Error Status:", s3Response.status);
                setStatus({ message: "Upload to Storage Failed", color: "red" });
            }

        } catch (error) {
            console.error("Upload process error:", error);
            setStatus({ message: "Error Uploading File: " + error.message, color: "red" });
        }
    };

    return(
        <div className="upload1">
            <h1>Upload File Here</h1>
            {/* Modified to use React state and event handlers */}
            <input type="file" className="file" id="fileInput" onChange={handleFileChange}/>
            <br/>
            <button className="uploadButton" onClick={handleUpload}>Upload</button>
            <p className="status" style={{ color: status.color }}>{status.message}</p>
        </div>
    )
}

export default Upload