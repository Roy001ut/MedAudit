# MedAudit: AI-Powered Medical Analysis

Analyze prescriptions, hospital bills, and lab reports using AI. Upload documents, detect billing fraud, get drug explanations, and track lab results — all with user-isolated data and JWT authentication.

---

## Features

- **Drug Analysis** — Enter a drug name and dosage to get plain-English explanations, what it treats, side effects, and red flags
- **Bill Audit** — Upload a hospital bill and get itemized charge review, overbilling detection, and a fraud risk score
- **Lab Reports** — Track lab results over time with normal range comparisons
- **Document OCR** — Upload PDFs or images; text is extracted automatically
- **Secure Auth** — JWT tokens, bcrypt passwords, per-user data isolation

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose
- A Claude API key from [console.anthropic.com](https://console.anthropic.com)

### 1. Clone and configure

```bash
git clone <repo-url>
cd MedAudit
```

Edit `.env` and fill in your API keys:

```bash
CLAUDE_API_KEY=sk-ant-YOUR_KEY_HERE
OPENAI_API_KEY=sk-YOUR_KEY_HERE
```

> The `.env` file is git-ignored. Never commit API keys.

### 2. Start all services

```bash
docker-compose up
```

Wait for `Application startup complete` in the logs (roughly 30–60 seconds for Postgres to initialize on first run).

### 3. Open in browser

| Service       | URL                              |
|---------------|----------------------------------|
| Frontend      | http://localhost:5173            |
| Backend API   | http://localhost:8000            |
| API Docs      | http://localhost:8000/docs       |

---

## API Quick Reference

### Register

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123","full_name":"Jane Doe"}'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123"}'
```

Response includes `access_token`, `expires_in`, and the `user` object.

### Authenticated request

```bash
TOKEN="your_token_here"

curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Upload a document

```bash
curl -X POST http://localhost:8000/api/documents/upload/bill \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/bill.pdf"
```

Valid document types: `prescription`, `bill`, `lab_report`, `consultation`, `insurance_policy`

### Analyze a drug

```bash
curl -X POST http://localhost:8000/api/analysis/drug \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"drug_name":"Metformin","dosage":"500mg"}'
```

### Analyze a bill

```bash
curl -X POST http://localhost:8000/api/analysis/bill \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"document_id":"<doc-uuid>","patient_diagnosis":"Type 2 Diabetes"}'
```

---

## Project Structure

```
MedAudit/
├── backend/
│   ├── app/
│   │   ├── config.py           # Settings loaded from .env
│   │   ├── main.py             # FastAPI app, CORS, routes
│   │   ├── dependencies.py     # JWT auth dependency injection
│   │   ├── api/
│   │   │   ├── routes/         # auth.py, documents.py, analysis.py
│   │   │   └── schemas/        # Pydantic request/response models
│   │   ├── services/
│   │   │   ├── auth_service.py     # bcrypt + JWT
│   │   │   ├── document_service.py # file upload + OCR
│   │   │   ├── drug_service.py     # Claude API
│   │   │   └── bill_service.py     # Claude API
│   │   ├── models/             # SQLAlchemy ORM models
│   │   └── database/           # engine, session, base
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Auth gate
│   │   ├── pages/Login.tsx     # Register + Login form
│   │   ├── components/Dashboard.tsx
│   │   ├── services/api.ts     # Axios + interceptors
│   │   └── store/auth.store.ts # Zustand + localStorage
│   └── Dockerfile
├── docker-compose.yml
├── .env                        # API keys (not committed)
└── README.md
```

---

## Troubleshooting

**Postgres not ready**
```bash
docker-compose logs postgres
# Wait for: "database system is ready to accept connections"
```

**Port already in use**
```bash
lsof -ti:5173 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

**Check tables were created**
```bash
docker-compose exec postgres psql -U medaudit -d medaudit_db -c "\dt"
```

**Frontend blank screen**
Open browser devtools (F12 → Console). Verify the backend is reachable:
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

**Claude API errors**
Confirm your key starts with `sk-ant-` and has sufficient credits at [console.anthropic.com](https://console.anthropic.com).

---

## Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | FastAPI, SQLAlchemy, PostgreSQL    |
| Auth      | JWT (PyJWT), bcrypt (passlib)      |
| AI        | Anthropic Claude API              |
| OCR       | Tesseract, pdfplumber, Pillow     |
| Frontend  | React, TypeScript, Vite           |
| Styling   | Tailwind CSS                      |
| State     | Zustand + localStorage            |
| Cache/MQ  | Redis                             |
| Deploy    | Docker Compose                    |
