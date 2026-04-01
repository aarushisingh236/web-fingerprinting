# 🚀 Web Server Fingerprinting Tool - Setup Guide

This project consists of a **Python Backend (Flask)** and a **React Frontend (Vite)**. It also includes a standalone **CLI Tool** for quick scans.

---

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [npm](https://www.npmjs.com/) (usually comes with Node.js)

---

## 📂 Project Structure

```text
web-fingerprinting/
├── backend/            # Flask API server
├── frontend/           # React + Vite UI
├── main.py             # CLI Tool
├── fingerprint_logic.py # Core logic (shared)
└── ...
```

---

## 🖥️ Backend Setup (Flask)

1. **Navigate to the root directory**:
   ```bash
   cd web-fingerprinting
   ```

2. **(Optional) Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Backend Server**:
   ```bash
   python backend/app.py
   ```
   The backend will start on **`http://localhost:5000`**.

---

## 🌐 Frontend Setup (React + Vite)

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Run the Development Server**:
   ```bash
   npm run dev
   ```
   The frontend will be available at **`http://localhost:5173`** (or the port shown in your terminal).

---

## ⌨️ CLI Tool (Standalone)

If you prefer using the terminal, you can run the scanner directly without the UI or Backend:

1. **Run a scan on specific targets**:
   ```bash
   python main.py google.com example.com
   ```

2. **View Results**:
   Results are saved to `results.txt` in the root directory.

---

## 📝 Notes
- Ensure port `5000` (Backend) and `5173` (Frontend) are not being used by other applications.
- If you encounter "Access Denied" or "CORS" errors, ensure the backend is running and `flask-cors` is installed.
