# Sales Insight Automator

> **A secure, containerized application that transforms raw sales data into AI-powered executive summaries — delivered straight to your inbox.**

Built as a rapid-prototype sprint exercise.

---

## Architecture

```
┌──────────────────┐     POST /api/analyze     ┌──────────────────┐
│   React SPA      │ ──────────────────────────▶│   FastAPI API     │
│   (Vite + React) │                            │                  │
│   Port 3000      │◀────── JSON Response ──────│   Port 8000      │
└──────────────────┘                            └────────┬─────────┘
                                                         │
                                          ┌──────────────┼──────────────┐
                                          ▼              ▼              ▼
                                    ┌──────────┐  ┌───────────┐  ┌──────────┐
                                    │  Pandas  │  │  Gemini   │  │  Resend  │
                                    │  Parser  │  │  LLM API  │  │  Email   │
                                    └──────────┘  └───────────┘  └──────────┘
```

**Tech Stack**: React + Vite · FastAPI + Python · Google Gemini (`gemini-2.0-flash`) · Resend Email API · Docker + Compose · GitHub Actions

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- API Keys: [Google Gemini](https://aistudio.google.com/apikey) + [Resend](https://resend.com)

### 1. Clone & Configure

```bash
git clone https://github.com/<your-username>/sales-insight-automator.git
cd sales-insight-automator

# Create your backend .env from the template
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your API keys:

```env
GEMINI_API_KEY=your_google_gemini_api_key
RESEND_API_KEY=your_resend_api_key
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

| Service    | URL                           |
| ---------- | ----------------------------- |
| Frontend   | http://localhost:3000          |
| Backend    | http://localhost:8000          |
| Swagger UI | http://localhost:8000/docs     |
| ReDoc      | http://localhost:8000/redoc    |

### 3. Run Without Docker (Development)

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Pydantic settings from .env
│   │   ├── models/
│   │   │   └── schemas.py       # Response models
│   │   ├── routers/
│   │   │   ├── analyze.py       # POST /api/analyze
│   │   │   └── health.py        # GET /api/health
│   │   └── services/
│   │       ├── ai_engine.py     # Gemini LLM integration
│   │       ├── email_service.py # Resend email delivery
│   │       └── parser.py        # CSV/XLSX → structured text
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main SPA component
│   │   ├── api/client.js        # API client
│   │   ├── components/
│   │   │   ├── UploadForm.jsx   # File + email form
│   │   │   └── StatusFeedback.jsx
│   │   └── index.css            # Design system
│   ├── Dockerfile
│   └── .env.example
├── .github/workflows/ci.yml    # CI/CD pipeline
├── docker-compose.yml
├── sales_q1_2026.csv           # Sample test data
└── README.md
```

---

## Security Overview

| Layer              | Implementation                                                  |
| ------------------ | --------------------------------------------------------------- |
| **Rate Limiting**  | `slowapi` — 10 requests/minute per IP on `/api/analyze`        |
| **CORS**           | Whitelist-only origins (configurable via `ALLOWED_ORIGINS`)     |
| **Input Validation** | File type/extension check, max file size (10 MB), Pydantic email validation |
| **Error Handling** | Global exception handler — no stack traces leaked to client     |
| **Container Security** | Non-root user in production Docker image                    |
| **Env Secrets**    | All API keys loaded from `.env`, never committed to git         |

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) triggers on **Pull Requests to `main`** and runs:

1. **Backend**: Python lint (`ruff`) → Docker image build
2. **Frontend**: ESLint → Vite production build

---

## API Documentation

Interactive Swagger UI is available at **[`/docs`](http://localhost:8000/docs)** when the backend is running.

### `POST /api/analyze`

| Parameter | Type       | Description                    |
| --------- | ---------- | ------------------------------ |
| `file`    | `File`     | CSV or XLSX sales data file    |
| `email`   | `string`   | Recipient email address        |

**Success Response** (`200`):
```json
{
  "success": true,
  "message": "Sales summary generated and emailed successfully!",
  "summary": "...",
  "recipient_email": "user@example.com"
}
```

### `GET /api/health`

Returns `{ "status": "healthy", "service": "Sales Insight Automator API", "version": "1.0.0" }`

---

## Testing

Use the provided `sales_q1_2026.csv` sample file:

1. Open http://localhost:3000
2. Upload the sample CSV
3. Enter a recipient email
4. Click **Generate & Send Report**
5. Check the inbox for the AI-generated executive brief

---

## Deployment

| Component | Platform | Notes |
| --- | --- | --- |
| Frontend | Vercel / Netlify | Set `VITE_API_URL` env var to deployed backend URL |
| Backend | Render | Set all env vars from `.env.example` |

---

## License

MIT — Built with ❤️