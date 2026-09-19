# Next.js AI Assistant — FDE Training

Full-stack TypeScript AI application training deliverable.

## Included
- App Router and file routing
- Server Components and Client Components
- Next.js API Routes
- Server Actions
- Streaming response demo
- Demo authentication with HTTP-only cookie
- Middleware route protection
- Server-side FastAPI integration
- Runtime validation for chat responses
- FastAPI simulated AI backend
- `.gitignore` and `.env.example`

## Local run

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
copy .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`.

Demo credentials: `demo-user` / `demo-password`.

The AI backend is intentionally simulated for training. Replace demo authentication with Microsoft Entra ID and the simulated model call with an approved enterprise AI service for production.
