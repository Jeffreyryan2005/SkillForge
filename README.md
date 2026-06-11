# SkillForge

SkillForge is an AI-powered Career Skill Gap Analyzer and 30-Day Learning Plan Generator. Paste your resume and a job description, and SkillForge will identify skill gaps, calculate your profile match, and provide a practical learning roadmap with free resources.

## Architecture

skillforge/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── Hero.tsx
│   │   ├── InputSection.tsx
│   │   ├── Results.tsx
│   │   ├── MatchScoreCircle.tsx
│   │   ├── SkillTags.tsx
│   │   ├── SkillRadarChart.tsx
│   │   └── LearningPlan.tsx
│   ├── types/
│   │   └── index.ts
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── next.config.ts
│   ├── tsconfig.json
│   └── next-env.d.ts

## Features

- AI-guided skill gap analysis using Groq llama-3.3-70b-versatile
- Resume and job description comparison
- Match score visualization with animated radial progress
- Skill gap cards, matched skill tags, and radar coverage chart
- Expandable 30-day learning plan with task resources
- Responsive Next.js 14 App Router frontend with TailwindCSS
 - PDF resume upload: upload a PDF resume and the backend will extract text for analysis
 - Mock analyzer fallback: if a Groq API key is not provided or the AI call fails, SkillForge returns a heuristic mock analysis so demos still work offline

## How GitHub Copilot Was Used

This project was scaffolded and implemented with GitHub Copilot assistance. Copilot helped generate the full-stack application structure, React components, Tailwind styling, API integration, and documentation.

## Local Setup

### Backend

1. Navigate to the backend folder:
   ```powershell
   cd backend
   ```
2. Create a virtual environment and install dependencies:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your Groq API key:
   ```powershell
   copy .env.example .env
   ```
4. Run the Flask backend:
   ```powershell
   python app.py
   ```
   Note: If you do not have a GROQ API key set, the backend will return a demo/mock analysis instead of calling the LLM. To use the live model, set `GROQ_API_KEY` in `backend/.env`.
5. Verify health:
   ```powershell
   curl http://127.0.0.1:5000/api/health
   ```

### Frontend

1. Navigate to the frontend folder:
   ```powershell
   cd frontend
   ```
2. Install packages:
   ```powershell
   npm install
   ```
3. Create `.env.local` with:
   ```text
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```
4. Start the Next.js app:
   ```powershell
   npm run dev
   ```
5. Open `http://localhost:3000` in your browser.

## Deployment

- Frontend: deploy to Vercel from the `frontend/` folder using `frontend/vercel.json`.
- Backend: deploy to Render from the repository root using `render.yaml`.

## Demo

After starting both services, visit the frontend and paste sample resume and job description text. Use the **Try Sample** button to populate example inputs instantly.

## ASCII Architecture Diagram

```
[Browser] --> [Next.js Frontend]
                     |
                     v
              [Flask Backend API]
                     |
                     v
                [Groq LLM Service]
```
