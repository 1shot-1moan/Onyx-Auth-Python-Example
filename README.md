# Onyx Gate â€” Python Example

> Official Python SDK and loader example for [Onyx Gate Auth](https://auth.script-kittens.com) â€” the authentication platform built for cheat developers.

![Python](https://img.shields.io/badge/Python-3.8+-3572A5?style=flat&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey?style=flat)
![Dependencies](https://img.shields.io/badge/Dependencies-requests-28a745?style=flat)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

---

## What is Onyx Gate?

Onyx Gate is a KeyAuth-style authentication system built by Script Kittens. It gives your cheat or tool:

- **HWID Lock** â€” bind each user to one machine
- **License Keys** â€” generate, sell, and track keys from the dashboard
- **Live Sessions** â€” see who's online right now, kick them instantly
- **Blacklist** â€” ban HWIDs, IPs, or usernames with one click
- **Variables** â€” push values to your app at runtime without recompiling
- **Plan Gating** â€” free vs paid feature separation built in

---

## Files

| File | Purpose |
|---|---|
| `skauth.py` | Core SDK â€” drop into **any** Python project |
| `loader.py` | Full console loader example |
| `requirements.txt` | Dependencies (`requests` only) |

---

## Requirements

- Python 3.8+
- `pip install requests`

---

## Quick Start

**1. Install dependencies**
```bash
pip install requests
```

**2. Set your App ID** â€” open `loader.py` and change line 20:
```python
APP_ID = "YOUR_APP_ID_HERE"
```
Get your App ID from [auth.script-kittens.com](https://auth.script-kittens.com) â†’ Manage Apps â†’ Credentials.

**3. Run**
```bash
python loader.py
```

---

## What customers see

```
==================================================
         Script Kittens â€” Internal Panel
           Powered by Onyx Gate Auth
==================================================

  [1] Login
  [2] Register  (need a license key)
  [3] Exit

  > 1

  LOGIN

  Username : potato
  Password : ********

  [OK] Authentication successful!

  +------------------------------------------+
  |  Username : potato                       |
  |  Plan     : PAID                         |
  |  Expires  : 29d 12h 44m 10s             |
  |  Email    : user@example.com             |
  +------------------------------------------+
```

---

## Integrate skauth.py into your own project

Copy `skauth.py` into your project, then:

```python
from skauth import SKAuth

# 1. Create auth object
auth = SKAuth("YOUR_APP_ID", "1.0")

# 2. Login
result = auth.login(username, password)
if result["ok"]:
    user = auth.user
    print(f"Welcome {user['username']}!")
    print(f"Plan: {user['plan']}")
else:
    print(f"Error: {result['message']}")
    exit(1)

# 3. Register (new customer with license key)
result = auth.register(username, password, email, license_key)

# 4. Gate paid features
if auth.user["plan"] in ["paid", "vip", "lifetime"]:
    launch_premium()
else:
    print("Upgrade required.")
    exit(1)

# 5. Fetch a server-side variable
val = auth.get_var("variable_name")
```

---

## Feature gating patterns

**Pattern A â€” Entire tool is paid only:**
```python
# Call after login
if auth.user["plan"] not in ["paid", "vip", "lifetime"]:
    print("This tool requires a paid plan.")
    print("Buy at discord.gg/tWwUSPh5GT")
    exit(1)
```

**Pattern B â€” Mixed free and paid features:**
```python
if choice == "1":
    run_free_feature()        # everyone can use this

elif choice == "2":
    if auth.user["plan"] in ["paid", "vip", "lifetime"]:
        run_premium_feature()
    else:
        print("Upgrade required â€” discord.gg/tWwUSPh5GT")
```

---

## Dashboard

Manage your users, keys, sessions, and blacklist at:
**[auth.script-kittens.com](https://auth.script-kittens.com)**

Buy keys or upgrade plans on our Discord:
**[discord.gg/tWwUSPh5GT](https://discord.gg/tWwUSPh5GT)**

---

## Other SDKs

| Language | Repo |
|---|---|
| C++ | [Onyx-Auth-CPP-Example](https://github.com/1shot-1moan/Onyx-Auth-CPP-Example) |
| C# WinForms | [Onyx-Auth-CSharp-Example](https://github.com/1shot-1moan/Onyx-Auth-CSharp-Example) |
