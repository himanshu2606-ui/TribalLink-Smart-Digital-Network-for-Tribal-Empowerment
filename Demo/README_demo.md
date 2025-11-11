# Demo — TribalLink (how to run)

This small README explains how to run the demo locally and verify the Home, Marketplace, and AgriHelpBot endpoints.

Pre-requisites
- Python 3.8+ installed
- (Recommended) a virtual environment placed at the repo root: `.venv`

Start the demo (PowerShell)
1. From the repo root, run:

```powershell
cd "Demo"
.\run_demo.ps1
```

This will try to activate `../.venv`, install packages from `requirements.txt` if present, and run `app.py`.

Quick manual commands

```powershell
# activate venv (if you use .venv at repo root)
& "C:\Users\<you>\...\TribalLink Smart Digital Network for Tribal Empowerment\.venv\Scripts\Activate.ps1"
cd "Demo"
python app.py
```

Endpoints to check
- Home: http://127.0.0.1:5000/
- Marketplace: http://127.0.0.1:5000/marketplace
- Products API: http://127.0.0.1:5000/api/products
- Chat API (POST): http://127.0.0.1:5000/api/chat (JSON body {"message":"hello"})

If pages show but your other devices cannot reach the server, ensure `app.py` uses `host='0.0.0.0'` (it does by default) and that Windows Firewall allows inbound TCP on port 5000.

If you want me to run verification steps or add a healthcheck script, tell me and I will add it.
