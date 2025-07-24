# LocalTube – Struktur Proyek

## Backend (Flask + yt-dlp)
- `app.py` – Entry point API
- `downloader.py` – Modul download video
- `database.py` – Simpan metadata video
- `videos/` – Folder hasil unduhan video

## Frontend (React + Vite + Tailwind)
- `src/pages/` – Halaman utama, player, dll
- `src/components/` – Komponen UI seperti form, video card
- `public/` – Static asset

## 📁 Struktur Folder

localtube/
├── backend/ ← Flask API untuk download & streaming video
├── frontend/ ← React UI yang menampilkan video
├── README.md ← Dokumentasi umum proyek

### 🔙 Backend (Flask)

backend/
├── app.py ← Entry point Flask
├── routes/
├── downloads/ ← Folder tempat menyimpan video
├── requirements.txt ← Dependensi backend

### 🎨 Frontend (React + Vite + Tailwind)

frontend/
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── vite.config.js
├── public/ ← Aset statis
├── src/
│ ├── App.jsx
│ ├── main.jsx
│ ├── index.css
│ ├── pages/
│ └── components/
└── node_modules/

## 🧪 Development Scripts

### Backend

= `python app.py`

### Frontend

= `npm run dev`