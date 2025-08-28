# eleva-# 🖨️ Print Shop Assistant – Flask (Codespaces Ready)

A minimal web app for a print shop that lets customers upload a file, select services (B/W, Color, Scan, Lamination, Binding), auto-calculates the bill, and generates a downloadable HTML invoice. Designed to run in **GitHub Codespaces**.

## Features
- File upload (stored in `uploads/`)
- Service selection with page/sheet counts
- Auto bill calculation
- Invoice generation (saved in `invoices/`)
- Download invoice from browser

> Note: Codespaces can't access your local printer. To actually print, download the uploaded file or invoice and print locally. Later, connect to a local print server (CUPS/Windows Spooler) via webhook/VPN.

## Quickstart (Codespaces)
```bash
pip install -r requirements.txt
python app.py
# Open forwarded port shown by Codespaces
```

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Environment variables (optional)
- `SECRET_KEY` – Flask secret (default: random dev)
- `UPLOAD_FOLDER` – where uploads are saved (default: `uploads`)
- `INVOICE_FOLDER` – where invoices are saved (default: `invoices`)
- `MAX_CONTENT_LENGTH_MB` – upload size limit (default: 25)

## Next steps
- Add Razorpay/Stripe checkout
- Add admin dashboard + order history (SQLite)
- Add webhook to a local print server
