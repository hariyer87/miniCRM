# MiniCRM Clinic

This project provides a FastAPI backend with a React + TypeScript frontend for a small diagnostic clinic CRM. Features include JWT authentication, patient management, visits, test orders/results, billing, audit logs, and a simple DICOM connector for Canon Xario 200 exports.

## Backend

### Setup

1. Create a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure environment variables in a `.env` file:
   ```env
   DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/minicrm
   SECRET_KEY=change-me
   DICOM_INBOX_DIR=./dicom_inbox
   DICOM_ARCHIVE_DIR=./dicom_archive
   ```
3. Run database migrations:
   ```bash
   alembic upgrade head
   ```
4. Seed sample data:
   ```bash
   python seed_data.py
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Notes
- The `DICOM_INBOX_DIR` is scanned every five minutes on startup; use `POST /imaging-studies/import-once` to trigger manual import.
- Authentication endpoints: `POST /auth/login` and `GET /auth/me`.

## Frontend

### Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run the development server:
   ```bash
   npm run dev
   ```
   The app expects the backend at `http://localhost:8000`.

### Build

```bash
npm run build
```

## Development Tips

- API routes live under `backend/app/api` and models under `backend/app/models`.
- Update Alembic revisions in `backend/app/alembic/versions` when the schema changes.
- Audit events are written automatically for key actions.
