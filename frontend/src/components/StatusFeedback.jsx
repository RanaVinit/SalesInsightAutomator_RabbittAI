export default function StatusFeedback({ status, summary, error, email, message, onReset }) {
    if (status === "success") {
        return (
            <div className="feedback feedback-success">
                <div className="feedback-icon">✅</div>
                <h3>{message.includes("skipped") ? "Analysis Complete!" : "Report Sent Successfully!"}</h3>
                <p className="feedback-subtitle">
                    {message.includes("skipped") ? (
                        <span style={{ color: "var(--warning)" }}>
                            AI Summary generated! <em>(Email delivery to {email} skipped due to demo sandbox limits)</em>
                        </span>
                    ) : (
                        <>The AI-generated summary has been emailed to <strong>{email}</strong>.</>
                    )}
                </p>

                {summary && (
                    <details className="summary-preview">
                        <summary>Preview Summary</summary>
                        <div className="summary-content">
                            {summary.split("\n").map((line, i) => (
                                <p key={i}>{line || <br />}</p>
                            ))}
                        </div>
                    </details>
                )}

                <button className="reset-btn" onClick={onReset}>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                        <path d="M3 3v5h5" />
                    </svg>
                    Analyze Another File
                </button>
            </div>
        );
    }

    if (status === "error") {
        return (
            <div className="feedback feedback-error">
                <div className="feedback-icon">❌</div>
                <h3>Something Went Wrong</h3>
                <p className="feedback-subtitle">{error}</p>
                <button className="reset-btn" onClick={onReset}>
                    Try Again
                </button>
            </div>
        );
    }

    return null;
}
