import requests
import hashlib
import uuid
import subprocess

class SKAuth:
    BASE = "https://auth.script-kittens.com"

    def __init__(self, app_id, version="1.0"):
        self.app_id  = app_id
        self.version = version
        self.user    = None
        self.hwid    = self._get_hwid()

    def _get_hwid(self):
        try:
            out = subprocess.check_output(
                "wmic diskdrive get SerialNumber", shell=True
            ).decode()
            return hashlib.sha256(out.strip().encode()).hexdigest()[:32]
        except:
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:32]

    def login(self, username, password):
        try:
            r = requests.post(f"{self.BASE}/sdk/login", json={
                "appId": self.app_id, "username": username,
                "password": password, "hwid": self.hwid, "version": self.version
            }, timeout=10)
            d = r.json()
            if d.get("ok"):
                self.user = d["user"]
            return d
        except Exception as e:
            return {"ok": False, "message": f"Connection error: {e}"}

    def register(self, username, password, email="", license_key=""):
        try:
            return requests.post(f"{self.BASE}/sdk/register", json={
                "appId": self.app_id, "username": username,
                "password": password, "email": email, "licenseKey": license_key
            }, timeout=10).json()
        except Exception as e:
            return {"ok": False, "message": f"Connection error: {e}"}

    def get_var(self, name):
        try:
            r = requests.get(f"{self.BASE}/sdk/variable",
                params={"appId": self.app_id, "name": name}, timeout=10)
            return r.json().get("value")
        except:
            return None
