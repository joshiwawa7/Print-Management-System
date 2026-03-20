#!/usr/bin/env python3
"""PMS terminal API client (interactive CLI).

Detailed usage and the original banner are in README_PMS_CLIENT.md.
"""

import requests
import sys
import os
from datetime import datetime

# ── Configuration ─────────────────────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:8000"  # Change this if your FastAPI server runs on a different host/port

# ── ANSI Color Codes ───────────────────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    MAGENTA = "\033[95m"
    DIM     = "\033[2m"

# ── Helpers ────────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    # Simple header (kept minimal for compatibility across terminals)
    print()
    print(f"{Color.CYAN}{Color.BOLD}Print Management System (PMS) - Terminal API Client{Color.RESET}")
    print(f"{Color.DIM}  Connected to: {BASE_URL}{Color.RESET}")
    print()

def divider():
    print(f"{Color.DIM}{'─' * 48}{Color.RESET}")

def success(msg):
    print(f"{Color.GREEN}  ✔  {msg}{Color.RESET}")

def error(msg):
    print(f"{Color.RED}  ✘  {msg}{Color.RESET}")

def info(msg):
    print(f"{Color.CYAN}  ℹ  {msg}{Color.RESET}")

def prompt(msg):
    return input(f"{Color.YELLOW}  ▶  {msg}{Color.RESET}").strip()

def format_order(order: dict):
    """Pretty-print a single order."""
    divider()
    print(f"  {Color.BOLD}{Color.WHITE}Order #{order['id']}{Color.RESET}")
    divider()
    print(f"  {Color.CYAN}Customer   :{Color.RESET} {order['customer_name']}")
    print(f"  {Color.CYAN}Pages      :{Color.RESET} {order['pages']}")
    print(f"  {Color.CYAN}Print Type :{Color.RESET} {order['print_type']}")
    print(f"  {Color.CYAN}Unit Price :{Color.RESET} ₱{order['unit_price']:.2f}")
    print(f"  {Color.CYAN}Total Price:{Color.RESET} {Color.BOLD}₱{order['total_price']:.2f}{Color.RESET}")
    created = order.get("created_at", "")
    try:
        dt = datetime.fromisoformat(created)
        created = dt.strftime("%B %d, %Y  %I:%M %p")
    except Exception:
        pass
    print(f"  {Color.CYAN}Created At :{Color.RESET} {created}")
    divider()

# ── API Functions ──────────────────────────────────────────────────────────────

def create_order():
    """POST /orders — Create a new print order."""
    print(f"\n{Color.BOLD}{Color.MAGENTA}  ── Create New Order ──{Color.RESET}\n")

    customer_name = prompt("Customer Name       : ")
    if not customer_name:
        error("Customer name cannot be empty.")
        return

    pages_str = prompt("Number of Pages     : ")
    try:
        pages = int(pages_str)
        if pages <= 0:
            raise ValueError
    except ValueError:
        error("Pages must be a positive integer.")
        return

    print(f"\n{Color.DIM}  Print types: bw (black_and_white), color (colored), photo (photo paper){Color.RESET}")
    print(f"  You can also type friendly names: 'black_and_white', 'colored', 'photo' or numbers: 1=bw, 2=color, 3=photo")
    pt_input = prompt("Print Type          : ")
    if not pt_input:
        error("Print type cannot be empty.")
        return

    def normalize_print_type(s: str) -> str | None:
        """Map a user's free-form input to one of: 'bw', 'color', 'photo'."""
        if not s:
            return None
        key = s.strip().lower()
        # normalize common separators and words
        key = key.replace('-', '_').replace(' ', '_')

        mapping = {
            # black & white
            'bw': 'bw', 'b/w': 'bw', 'black_and_white': 'bw', 'blackandwhite': 'bw', 'black': 'bw',
            'black&white': 'bw', 'black_white': 'bw', '1': 'bw',
            # color
            'color': 'color', 'coloured': 'color', 'colored': 'color', 'colour': 'color', 'c': 'color', 'col': 'color', '2': 'color',
            # photo
            'photo': 'photo', 'photo_paper': 'photo', 'photopaper': 'photo', 'photo-paper': 'photo', 'p': 'photo', '3': 'photo',
        }

        # direct map
        if key in mapping:
            return mapping[key]

        # try removing underscores (e.g. user typed 'blackandwhite')
        key2 = key.replace('_', '')
        if key2 in mapping:
            return mapping[key2]

        return None

    print_type = normalize_print_type(pt_input)
    if not print_type:
        error("Invalid print type. Accepted values: bw (black_and_white), color (colored), photo (photo paper). Try: bw, color, photo")
        return

    payload = {
        "customer_name": customer_name,
        "pages": pages,
        "print_type": print_type,
    }

    print()
    info("Sending order to server...")

    try:
        response = requests.post(f"{BASE_URL}/orders", json=payload, timeout=10)
        if response.status_code == 200 or response.status_code == 201:
            order = response.json()
            success("Order created successfully!")
            format_order(order)
        elif response.status_code == 400:
            detail = response.json().get("detail", "Bad request.")
            error(f"Bad Request: {detail}")
        else:
            error(f"Unexpected response [{response.status_code}]: {response.text}")
    except requests.exceptions.ConnectionError:
        error(f"Cannot connect to the server at {BASE_URL}.")
        info("Make sure your FastAPI server is running.")
    except requests.exceptions.Timeout:
        error("Request timed out. The server took too long to respond.")
    except Exception as e:
        error(f"An error occurred: {e}")

def get_order():
    """GET /orders/{order_id} — Get a specific order by ID."""
    print(f"\n{Color.BOLD}{Color.MAGENTA}  ── Get Order by ID ──{Color.RESET}\n")

    order_id_str = prompt("Enter Order ID: ")
    try:
        order_id = int(order_id_str)
    except ValueError:
        error("Order ID must be a number.")
        return

    info(f"Fetching order #{order_id}...")

    try:
        response = requests.get(f"{BASE_URL}/orders/{order_id}", timeout=10)
        if response.status_code == 200:
            order = response.json()
            success("Order found!")
            format_order(order)
        elif response.status_code == 404:
            error(f"Order #{order_id} not found.")
        else:
            error(f"Unexpected response [{response.status_code}]: {response.text}")
    except requests.exceptions.ConnectionError:
        error(f"Cannot connect to the server at {BASE_URL}.")
        info("Make sure your FastAPI server is running.")
    except requests.exceptions.Timeout:
        error("Request timed out.")
    except Exception as e:
        error(f"An error occurred: {e}")

def list_orders():
    """GET /orders — List recent orders."""
    print(f"\n{Color.BOLD}{Color.MAGENTA}  ── List Recent Orders ──{Color.RESET}\n")

    limit_str = prompt("How many orders to show? (1-100, default=10): ")
    if limit_str == "":
        limit = 10
    else:
        try:
            limit = int(limit_str)
            if not (1 <= limit <= 100):
                raise ValueError
        except ValueError:
            error("Limit must be a number between 1 and 100.")
            return

    info(f"Fetching last {limit} orders...")

    try:
        response = requests.get(f"{BASE_URL}/orders", params={"limit": limit}, timeout=10)
        if response.status_code == 200:
            orders = response.json()
            if not orders:
                info("No orders found.")
                return
            success(f"Found {len(orders)} order(s).\n")
            for order in orders:
                format_order(order)
                print()
        else:
            error(f"Unexpected response [{response.status_code}]: {response.text}")
    except requests.exceptions.ConnectionError:
        error(f"Cannot connect to the server at {BASE_URL}.")
        info("Make sure your FastAPI server is running.")
    except requests.exceptions.Timeout:
        error("Request timed out.")
    except Exception as e:
        error(f"An error occurred: {e}")

def check_connection():
    """Quick health check — try to reach GET /orders."""
    try:
        response = requests.get(f"{BASE_URL}/orders", params={"limit": 1}, timeout=5)
        if response.status_code == 200:
            success(f"Successfully connected to PMS server at {BASE_URL}")
        else:
            error(f"Server responded with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        error(f"Could not connect to {BASE_URL}")
        info("Make sure your FastAPI server is running with: uvicorn app.main:app --reload")
    except Exception as e:
        error(f"Connection check failed: {e}")

# ── Main Menu ──────────────────────────────────────────────────────────────────

def main_menu():
    while True:
        banner()
        print(f"  {Color.BOLD}MAIN MENU{Color.RESET}\n")
        print(f"  {Color.WHITE}[1]{Color.RESET}  Create a New Order")
        print(f"  {Color.WHITE}[2]{Color.RESET}  Get Order by ID")
        print(f"  {Color.WHITE}[3]{Color.RESET}  List Recent Orders")
        print(f"  {Color.WHITE}[4]{Color.RESET}  Check Server Connection")
        print(f"  {Color.WHITE}[0]{Color.RESET}  Exit")
        print()

        choice = prompt("Choose an option: ")

        if choice == "1":
            create_order()
        elif choice == "2":
            get_order()
        elif choice == "3":
            list_orders()
        elif choice == "4":
            check_connection()
        elif choice == "0":
            print(f"\n{Color.CYAN}  Goodbye! 👋{Color.RESET}\n")
            sys.exit(0)
        else:
            error("Invalid option. Please choose 1, 2, 3, 4, or 0.")

        print()
        input(f"{Color.DIM}  Press ENTER to return to the menu...{Color.RESET}")
        clear()

# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Color.CYAN}  Interrupted. Goodbye! 👋{Color.RESET}\n")
        sys.exit(0)
