# Print Management System (PMS) - Backend Scaffold

This is a minimal FastAPI backend scaffold for the Print Management System described in `PRD.txt`.

Features included:
- POST /orders : create an order (unit_price and total_price calculated automatically)
- GET /orders/{id} : fetch a single order
- GET /orders?limit=N : fetch recent orders (default 10)

Prices (per PRD):
- Black and white: ₱2 per page (print_type: "bw")
- Colored: ₱5 per page (print_type: "color")
- Photo paper: ₱20 per page (print_type: "photo")

Quick start (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# run server
uvicorn app.main:app --reload
```

Run tests:

```powershell
pip install -r requirements.txt
pytest -q
```

Client
------
This repository includes a simple terminal-based API client. See `README_PMS_CLIENT.md` for usage and demo instructions.

