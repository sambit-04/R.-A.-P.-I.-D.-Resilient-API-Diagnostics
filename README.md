R. A. P. I. D. Resilient API Diagnostics - Full prototype
Folders:
- backend/: Flask backend (serves static backend and API test logics)
- frontend/: React + Tailwind + Node JS (serves frontend and API endpoints)

Quick backend start
1. Open terminal and go to backend folder:
   cd C:\Users\sambi\OneDrive\Documents\Major Project\R. A. P. I. D\backend
   cd backend
2. Create venv and activate:
   python -m venv venv
   .\venv\Scripts\Activate
3. Install dependencies:
   pip install -r requirements.txt
4. Run server:
   python app.py
5. Open http://127.0.0.1:5000/ in your browser.

Quick frontend start

## Prerequisites
- Node.js 18+ and npm
- Backend running at http://127.0.0.1:5000 (Flask server with /api endpoints)

1. Open another terminal and go to frontend folder:
   cd C:\Users\sambi\OneDrive\Documents\Major Project\R. A. P. I. D\frontend
   cd frontend
2. Install file:
   npm install
3. Run webapp:
   npm run dev
4. The Vite dev server opens (by default) at http://localhost:3000.
