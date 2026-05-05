"""
 Onyx Gate — Python Loader Example
 ===================================
 HOW TO USE:
   1. Change APP_ID below to your App ID from the dashboard
   2. Change APP_VERSION to match your app version
   3. Run:  pip install requests
   4. Run:  python loader.py

 WHAT TO DO AFTER LOGIN SUCCEEDS:
   - Replace the "YOUR CHEAT CODE HERE" section at the bottom
     with whatever your tool/script actually does.
"""

import os
import sys
from skauth import SKAuth   # skauth.py must be in the same folder

# ─── CONFIG — change these ────────────────────────────────────────────────────
APP_ID      = "YOUR_APP_ID_HERE"   # paste your App ID from dashboard
APP_VERSION = "1.0"                # must match version set in dashboard
# ─────────────────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print("=" * 50)
    print("         Script Kittens — Internal Panel")
    print("           Powered by Onyx Gate Auth")
    print("=" * 50)
    print()

def login_screen(auth):
    while True:
        banner()
        print("  [1] Login")
        print("  [2] Register (need a license key)")
        print("  [3] Exit")
        print()
        choice = input("  Choice: ").strip()

        if choice == "1":
            banner()
            print("  LOGIN")
            print()
            username = input("  Username : ").strip()
            password = input("  Password : ").strip()

            print()
            print("  Authenticating...")

            result = auth.login(username, password)

            if result["ok"]:
                return result   # success — proceed to main()
            else:
                print()
                print(f"  ✗ {result['message']}")
                input("  Press Enter to try again...")

        elif choice == "2":
            banner()
            print("  REGISTER")
            print()
            username    = input("  Choose username : ").strip()
            password    = input("  Choose password : ").strip()
            email       = input("  Email (optional): ").strip()
            license_key = input("  License key     : ").strip()

            print()
            print("  Creating account...")

            result = auth.register(username, password, email, license_key)

            if result["ok"]:
                print()
                print("  ✓ Account created! Login now.")
            else:
                print()
                print(f"  ✗ {result['message']}")
            input("  Press Enter to continue...")

        elif choice == "3":
            sys.exit(0)

def is_paid(auth):
    """Returns True if user has an active paid plan."""
    return auth.user.get("plan", "free") in ["paid", "vip", "lifetime"]

def require_paid(auth):
    """Call this at startup if your ENTIRE tool requires a paid plan."""
    if not is_paid(auth):
        print("  You need a paid plan for this tool.")
        print("  Buy at: discord.gg/tWwUSPh5GT")
        input("  Press Enter to exit...")
        sys.exit(1)

def main():
    # Initialize auth
    auth = SKAuth(APP_ID, APP_VERSION)

    # Show login screen until success
    login_screen(auth)

    # ─── Logged in ─────────────────────────────────────────────
    banner()
    u = auth.user
    plan    = u.get("plan", "free")
    expires = u.get("expires") or "Never"
    email   = u.get("email") or "—"

    print(f"  [OK] Authentication successful!\n")
    print(f"  +------------------------------------------+")
    print(f"  |  Username : {u['username']:<28}|")
    print(f"  |  Plan     : {plan:<28}|")
    print(f"  |  Expires  : {expires:<28}|")
    print(f"  |  Email    : {email:<28}|")
    print(f"  +------------------------------------------+\n")

    # Get a server-side variable (set in dashboard → Settings → Variables)
    motd = auth.get_var("message")
    if motd:
        print(f"  Server: {motd}\n")

    # ── OPTION A: whole tool is paid only — uncomment to use ──────────────────
    # require_paid(auth)

    # ── OPTION B: mixed free/paid features — handled per-feature below ─────────
    print()
    print("  Loading cheat...")
    input("  Press Enter to continue...")

    # ─── YOUR CHEAT CODE HERE ───────────────────────────────────
    # Replace everything below with your actual tool logic.
    # auth.user["plan"]     = their plan (free/paid/vip/lifetime)
    # auth.user["username"] = their username
    # auth.user["expires"]  = expiry date
    # auth.get_var("name")  = fetch a server-side variable

    banner()
    print("  Cheat menu:")
    print("  [1] Feature 1 (free)")
    print("  [2] Feature 2 (paid only)")
    print("  [3] Exit")
    print()

    while True:
        choice = input("  > ").strip()
        if choice == "1":
            print("  Running feature 1...")
        elif choice == "2":
            if is_paid(auth):
                print("  Running premium feature 2...")
            else:
                print("  Upgrade required. Buy at discord.gg/tWwUSPh5GT")
        elif choice == "3":
            sys.exit(0)

if __name__ == "__main__":
    main()
