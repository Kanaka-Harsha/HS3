function Upload()
{
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
    }
    return(
        <div className="upload">
            <h1>Upload</h1>
            <input type="file" className="file" id="fileInput"/>
            <br/>
            <button className="uploadButton" onClick={uploadFile}>Upload</button>
            <p className="status"></p>
        </div>
    )
}

export default Upload