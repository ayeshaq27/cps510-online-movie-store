# Web version: Customer Service Login

This folder contains a small Flask app that provides an HTML login form and a JSON API to authenticate customer-service employees.

Files added:
- `web_cs_login.py` - Flask app (routes `/` and `/login`, plus `/api/login`)
- `templates/cs_login.html` - HTML login form
- `templates/login_result.html` - Simple result page
- `requirements.txt` - Minimal dependencies

Quick start (PowerShell):

```powershell
# Activate your virtual environment (if using one)
.\venv_name\Scripts\Activate.ps1
pip install -r requirements.txt
python web_cs_login.py
# Open http://127.0.0.1:5000 in your browser
```

Notes:
- `web_cs_login.py` uses `connect.get_connection()` (same as the GUI version) so ensure your DB connection configuration works for the server process.
- Replace `app.secret_key` before deploying to production.
