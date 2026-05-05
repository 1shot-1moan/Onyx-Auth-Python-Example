# Onyx Gate — Python Loader Example

## Requirements
- Python 3.8+
- pip install requests

## Setup (2 steps)
1. Open `loader.py` — change `APP_ID` to your App ID from the Onyx Gate dashboard
2. Run: `python loader.py`

## Files
| File | Purpose |
|------|---------|
| `skauth.py` | SDK — don't edit |
| `loader.py` | Your loader — edit this |
| `requirements.txt` | Dependencies |

## Add to your own script
```python
from skauth import SKAuth
auth = SKAuth("YOUR_APP_ID")
result = auth.login(username, password)
if result["ok"]:
    print("Logged in!")  # launch your tool
```
