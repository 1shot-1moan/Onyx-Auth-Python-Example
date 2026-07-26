import requests
import hashlib
import uuid
import subprocess
import ctypes
import os
import threading
import time

class SKAuth:
    BASE = "https://auth.script-kittens.com"

    def __init__(self, app_id, version="1.0"):
        self.app_id  = app_id
        self.version = version
        self.user    = None
        self.hwid    = self._get_hwid()
        self.check_security()
        self.init()
        self._start_anti_dll_injection_monitor()

    def init(self):
        return self.checkblack()

    def checkblack(self):
        try:
            r = requests.post(f"{self.BASE}/sdk/init", json={
                "appId": self.app_id, "hwid": self.hwid, "version": self.version
            }, timeout=10)
            d = r.json()
            if not d.get("ok"):
                msg = d.get("message") or "Access Denied: Your HWID or IP address is blacklisted."
                if os.name == 'nt':
                    ctypes.windll.user32.MessageBoxW(0, msg, "Onyx Gate Security — Access Denied", 0x10)
                os._exit(0)
                return False
        except Exception:
            pass
        return True

    def checkban(self, username):
        if not username:
            return False
        try:
            r = requests.post(f"{self.BASE}/sdk/check-ban", json={
                "appId": self.app_id, "username": username
            }, timeout=10)
            d = r.json()
            if not d.get("ok"):
                msg = d.get("message") or "Account banned. Contact support."
                if os.name == 'nt':
                    ctypes.windll.user32.MessageBoxW(0, msg, "Onyx Gate Security — Account Banned", 0x10)
                os._exit(0)
                return True
        except Exception:
            pass
        return False

    def _get_loaded_modules(self):
        modules = set()
        if os.name == 'nt':
            try:
                hProcess = ctypes.windll.kernel32.GetCurrentProcess()
                hMods = (ctypes.c_void_p * 1024)()
                cbNeeded = ctypes.c_ulong()
                if ctypes.windll.psapi.EnumProcessModules(hProcess, ctypes.byref(hMods), ctypes.sizeof(hMods), ctypes.byref(cbNeeded)):
                    count = int(cbNeeded.value / ctypes.sizeof(ctypes.c_void_p))
                    modName = (ctypes.c_char * 260)()
                    modPath = (ctypes.c_char * 260)()
                    for i in range(count):
                        if ctypes.windll.psapi.GetModuleFileNameExA(hProcess, hMods[i], ctypes.byref(modPath), 260):
                            full_path = modPath.value.decode("utf-8", errors="ignore").lower()
                            if "\\windows\\system32\\" in full_path or "\\windows\\syswow64\\" in full_path or "\\windows\\winsxs\\" in full_path:
                                continue
                        if ctypes.windll.psapi.GetModuleBaseNameA(hProcess, hMods[i], ctypes.byref(modName), 260):
                            modules.add(modName.value.decode("utf-8", errors="ignore").lower())
            except:
                pass
        return modules

    def _start_anti_dll_injection_monitor(self):
        def monitor():
            if os.name != 'nt':
                return

            allowed_modules = set()

            def add_modules_to_allowed():
                try:
                    hProcess = ctypes.windll.kernel32.GetCurrentProcess()
                    hMods = (ctypes.c_void_p * 1024)()
                    cbNeeded = ctypes.c_ulong()
                    if ctypes.windll.psapi.EnumProcessModules(hProcess, ctypes.byref(hMods), ctypes.sizeof(hMods), ctypes.byref(cbNeeded)):
                        count = int(cbNeeded.value / ctypes.sizeof(ctypes.c_void_p))
                        modPath = (ctypes.c_char * 260)()
                        for i in range(count):
                            if ctypes.windll.psapi.GetModuleFileNameExA(hProcess, hMods[i], ctypes.byref(modPath), 260):
                                allowed_modules.add(modPath.value.decode("utf-8", errors="ignore").upper())
                except:
                    pass

            # Warmup phase (10 ticks x 500ms = 5s): continuously expand allowed snapshot while app initializes
            for _ in range(10):
                add_modules_to_allowed()
                time.sleep(0.5)

            # Active monitoring phase: check for unknown non-system DLLs injected after warmup
            while True:
                time.sleep(1.5)
                try:
                    hProcess = ctypes.windll.kernel32.GetCurrentProcess()
                    hMods = (ctypes.c_void_p * 1024)()
                    cbNeeded = ctypes.c_ulong()
                    if not ctypes.windll.psapi.EnumProcessModules(hProcess, ctypes.byref(hMods), ctypes.sizeof(hMods), ctypes.byref(cbNeeded)):
                        continue

                    count = int(cbNeeded.value / ctypes.sizeof(ctypes.c_void_p))
                    modName = (ctypes.c_char * 260)()
                    modPath = (ctypes.c_char * 260)()
                    triggered = None

                    for i in range(count):
                        path = ""
                        name = ""
                        if ctypes.windll.psapi.GetModuleFileNameExA(hProcess, hMods[i], ctypes.byref(modPath), 260):
                            path = modPath.value.decode("utf-8", errors="ignore")
                        if ctypes.windll.psapi.GetModuleBaseNameA(hProcess, hMods[i], ctypes.byref(modName), 260):
                            name = modName.value.decode("utf-8", errors="ignore")

                        upper = path.upper()

                        # Skip trusted Windows system & Program Files directories
                        if "C:\\WINDOWS\\" in upper or "C:\\PROGRAM FILES\\" in upper or "C:\\PROGRAM FILES (X86)\\" in upper:
                            continue

                        # Skip DLLs that were part of the initial warmup snapshot
                        if upper in allowed_modules:
                            continue

                        # Foreign/unauthorized DLL injected!
                        triggered = name or path
                        break

                    if triggered:
                        self.report_security_flag("dll_injection_detected", f"Unauthorized DLL injected: {triggered}")
                        time.sleep(0.4)
                        os._exit(0)
                except:
                    pass

        threading.Thread(target=monitor, daemon=True).start()

    def _get_hwid(self):
        try:
            out = subprocess.check_output(
                "wmic diskdrive get SerialNumber", shell=True
            ).decode()
            return hashlib.sha256(out.strip().encode()).hexdigest()[:32]
        except:
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:32]

    def report_security_flag(self, flag_type, details=""):
        """Sends client security telemetry to Onyx Gate Security Radar."""
        try:
            username = (self.user or {}).get("username", "Unknown")
            requests.post(f"{self.BASE}/sdk/security-flag", json={
                "appId": self.app_id,
                "username": username,
                "hwid": self.hwid,
                "flagType": flag_type,
                "details": details
            }, timeout=5)
        except:
            pass

    def check_security(self):
        """Native Win32 anti-debugger and blacklisted process scan."""
        try:
            if os.name == 'nt':
                if ctypes.windll.kernel32.IsDebuggerPresent():
                    self.report_security_flag("debugger_detected", "Win32 IsDebuggerPresent() returned True")
                    return False
                
                blacklisted = ["x64dbg.exe", "x32dbg.exe", "cheatengine-x86_64.exe", "ida64.exe", "processhacker.exe"]
                cmd = 'tasklist /FI "STATUS eq RUNNING"'
                output = subprocess.check_output(cmd, shell=True).decode().lower()
                for proc in blacklisted:
                    if proc in output:
                        self.report_security_flag("blacklisted_process", f"Detected process: {proc}")
                        return False
        except:
            pass
        return True

    def login(self, username, password):
        self.check_security()
        try:
            r = requests.post(f"{self.BASE}/sdk/login", json={
                "appId": self.app_id, "username": username,
                "password": password, "hwid": self.hwid, "version": self.version
            }, timeout=10)
            d = r.json()
            if d.get("ok"):
                self.user = d["user"]
            else:
                msg = d.get("message", "")
                if "banned" in msg.lower() or "blacklisted" in msg.lower():
                    if os.name == 'nt':
                        ctypes.windll.user32.MessageBoxW(0, msg, "Onyx Gate Security — Account Banned", 0x10)
                    os._exit(0)
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

    def validate(self):
        """Heartbeat — call periodically to kick banned/expired users + sync plan changes."""
        self.check_security()
        try:
            api_key = (self.user or {}).get("apiKey", "")
            r = requests.post(f"{self.BASE}/sdk/validate", json={
                "appId": self.app_id, "apiKey": api_key, "hwid": self.hwid
            }, timeout=10).json()
            if r.get("ok") and self.user:
                self.user["plan"]    = r.get("plan",    self.user.get("plan"))
                self.user["expires"] = r.get("expires", self.user.get("expires"))
            return r
        except Exception as e:
            return {"ok": False, "message": f"Connection error: {e}"}

    def is_paid(self):
        plan = (self.user or {}).get("plan", "free")
        return plan not in ("free", "")

    def get_var(self, name):
        try:
            r = requests.get(f"{self.BASE}/sdk/variable",
                params={"appId": self.app_id, "name": name}, timeout=10)
            return r.json().get("value")
        except:
            return None

# ── Quick start ─────────────────────────────────────────────────────────────
# pip install requests
auth = SKAuth("6a6356f72c9481f42186ef1b", "1.0")
result = auth.login("username", "password")
if result["ok"]:
    print(f"Welcome {auth.user['username']}! Plan: {auth.user['plan']}")
else:
    print(f"Error: {result['message']}")
    exit(1)