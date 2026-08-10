[README.md](https://github.com/user-attachments/files/30897408/README.md)
# API Vulnerability Tester — Frontend (React + Tailwind)

## Prerequisites
- Node.js 18+ and npm
- Backend running at http://127.0.0.1:5000 (Flask server with /api endpoints)

## Install
1. Open terminal in `frontend/`
2. Install:
   ```bash
   npm install
Run (dev)
bash
Copy code
npm run dev
The Vite dev server opens (by default) at http://localhost:3000.

What it does
Diagnostic Tool: start tests (basic, stress, fuzz), show live progress, and view results.

Diagnostic History: fetches /api/history and shows saved runs.

Notes
Tailwind is used for styling (dark theme).

The frontend polls /api/status/<task_id> to show live progress; ensure the Flask backend supports that endpoint.

For production, build with npm run build and serve the dist/.

yaml
Copy code

---

## Final instructions — where to paste and how to run

1. Create `frontend/` folder.
2. Create these files and subfolders exactly as shown (`src/`, `src/components/`, `public/` if you want).
3. Open terminal in `frontend/`:
npm install
npm run dev

sql
Copy code
4. Make sure your **Flask backend** is running at `http://127.0.0.1:5000` (the code I provided earlier uses `/api/*` endpoints). The frontend uses that base by default.
5. Open `http://localhost:3000` (or the URL Vite prints).
