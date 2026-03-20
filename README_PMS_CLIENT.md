# PMS Terminal API Client

This README documents the terminal-based API client `pms_client.py` used to interact with the Print Management System (PMS) FastAPI backend.

Overview
--------
The client is a small interactive command-line program that can:

- Create a new print order (POST /orders)
- Fetch an order by ID (GET /orders/{id})
- List recent orders (GET /orders)
- Check server connectivity

Usage
-----
Run the client from the project root (ensure your venv is active and the server is running):

```powershell
python pms_client.py
```

Interactive menu options:

- 1 : Create a New Order
- 2 : Get Order by ID
- 3 : List Recent Orders
- 4 : Check Server Connection
- 0 : Exit

Print type inputs
-----------------
The backend expects values: `bw`, `color`, or `photo`.
The client accepts friendly inputs and maps them to the backend codes (examples):

- Black & white: `bw`, `b/w`, `black_and_white`, `blackandwhite`, `black`, `black&white`, `1`
- Color: `color`, `colored`, `coloured`, `colour`, `2`
- Photo paper: `photo`, `photo_paper`, `photopaper`, `3`

Examples
--------
Create a 3-page black-and-white order for Alice:

1) Start the server:

```powershell
uvicorn app.main:app --reload
```

2) Run the client in another terminal and choose:

```
1
Alice
3
bw
```

Notes
-----
- The client prints a cosmetic banner and colored output. If your terminal does not render box-drawing characters or emoji, the text still works fine.
- The README contains the original banner and usage that were previously in `pms_client.py`.
