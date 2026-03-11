/**
 * API client for the Sales Insight Automator backend.
 */

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Upload a sales data file and trigger AI analysis + email delivery.
 * @param {File} file - The CSV/XLSX file to analyze
 * @param {string} email - Recipient email address
 * @returns {Promise<object>} API response with summary
 */
export async function analyzeSalesData(file, email) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("email", email);

  const response = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "An unexpected error occurred.");
  }

  return data;
}

/**
 * Check backend health.
 * @returns {Promise<object>}
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE}/api/health`);
  return response.json();
}
