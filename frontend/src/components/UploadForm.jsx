import { useState, useRef } from "react";

const ACCEPTED_TYPES = [
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
];

const ACCEPTED_EXTENSIONS = [".csv", ".xlsx", ".xls"];

export default function UploadForm({ onSubmit, isLoading }) {
    const [file, setFile] = useState(null);
    const [email, setEmail] = useState("");
    const [dragActive, setDragActive] = useState(false);
    const [fileError, setFileError] = useState("");
    const inputRef = useRef(null);

    const validateFile = (f) => {
        const ext = "." + f.name.split(".").pop().toLowerCase();
        if (!ACCEPTED_EXTENSIONS.includes(ext) && !ACCEPTED_TYPES.includes(f.type)) {
            setFileError("Please upload a .csv or .xlsx file.");
            return false;
        }
        if (f.size > 10 * 1024 * 1024) {
            setFileError("File is too large. Maximum 10 MB.");
            return false;
        }
        setFileError("");
        return true;
    };

    const handleFile = (f) => {
        if (validateFile(f)) {
            setFile(f);
        }
    };

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
        else if (e.type === "dragleave") setDragActive(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!file || !email) return;
        onSubmit(file, email);
    };

    const formatFileSize = (bytes) => {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
        return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    };

    return (
        <form className="upload-form" onSubmit={handleSubmit}>
            {/* Drop Zone */}
            <div
                className={`drop-zone ${dragActive ? "drag-active" : ""} ${file ? "has-file" : ""}`}
                onDragEnter={handleDrag}
                onDragOver={handleDrag}
                onDragLeave={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current?.click()}
            >
                <input
                    ref={inputRef}
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={(e) => e.target.files[0] && handleFile(e.target.files[0])}
                    hidden
                    id="file-upload"
                />

                {file ? (
                    <div className="file-info">
                        <div className="file-icon">📄</div>
                        <div className="file-details">
                            <span className="file-name">{file.name}</span>
                            <span className="file-size">{formatFileSize(file.size)}</span>
                        </div>
                        <button
                            type="button"
                            className="remove-file"
                            onClick={(e) => {
                                e.stopPropagation();
                                setFile(null);
                                setFileError("");
                            }}
                        >
                            ✕
                        </button>
                    </div>
                ) : (
                    <div className="drop-placeholder">
                        <div className="upload-icon">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                <polyline points="17 8 12 3 7 8" />
                                <line x1="12" y1="3" x2="12" y2="15" />
                            </svg>
                        </div>
                        <p className="drop-text">
                            <span className="drop-highlight">Click to upload</span> or drag & drop
                        </p>
                        <p className="drop-hint">CSV or XLSX files up to 10 MB</p>
                    </div>
                )}
            </div>
            {fileError && <p className="field-error">{fileError}</p>}

            {/* Email Input */}
            <div className="input-group">
                <label htmlFor="email-input">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="2" y="4" width="20" height="16" rx="2" />
                        <path d="m22,4-10,8L2,4" />
                    </svg>
                    Recipient Email
                </label>
                <input
                    id="email-input"
                    type="email"
                    placeholder="executive@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    disabled={isLoading}
                    className={emailError ? "error" : ""}
                />
                {emailError && <span className="error-message">{emailError}</span>}
                <span className="sandbox-note">
                    ⚠️ Note: Demo is sandboxed. You must use this email: "ranavinit1307@gmail.com".
                </span>
            </div>

            {/* Submit */}
            <button
                type="submit"
                className="submit-btn"
                disabled={!file || !email || isLoading}
                id="submit-analyze"
            >
                {isLoading ? (
                    <>
                        <span className="spinner" />
                        Analyzing...
                    </>
                ) : (
                    <>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M22 2L11 13" />
                            <path d="M22 2L15 22L11 13L2 9L22 2Z" />
                        </svg>
                        Generate & Send Report
                    </>
                )}
            </button>
        </form>
    );
}
