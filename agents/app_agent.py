import subprocess
import os

# Map of app names → executable paths
# Add your own apps here da
APP_MAP = {
    # Dev tools
    "vs code": r"C:\Users\System_1\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode": r"C:\Users\System_1\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "code": r"C:\Users\System_1\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "terminal": "powershell.exe",
    "powershell": "powershell.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",

    # Browsers
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "browser": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",

    # Your apps
    "spotify": r"C:\Users\System_1\AppData\Roaming\Spotify\Spotify.exe",
    "discord": r"C:\Users\System_1\AppData\Local\Discord\app-1.0.9173\Discord.exe",
    "ollama": "ollama",
}

class AppAgent:
    def execute(self, action: str, params: dict) -> str:
        action = action.lower()

        if any(x in action for x in ["open", "launch", "start", "run"]):
            app = params.get("app_name", "") or params.get("app", "")
            return self.open_app(app)

        elif any(x in action for x in ["close", "kill", "stop"]):
            app = params.get("app_name", "") or params.get("app", "")
            return self.close_app(app)

        return "App agent ready da"

    def open_app(self, app_name: str) -> str:
        if not app_name:
            return "No app name given da"

        app_lower = app_name.lower().strip()

        # Find in map
        for key, path in APP_MAP.items():
            if key in app_lower or app_lower in key:
                try:
                    subprocess.Popen([path])
                    return f"✅ Launched: {key}"
                except FileNotFoundError:
                    return f"❌ App not found at path: {path} — update APP_MAP da"
                except Exception as e:
                    return f"❌ Error launching {key}: {str(e)}"

        # Try running directly as command
        try:
            subprocess.Popen([app_name])
            return f"✅ Launched: {app_name}"
        except:
            return f"❌ App '{app_name}' not found da — add it to APP_MAP in app_agent.py"

    def close_app(self, app_name: str) -> str:
        try:
            subprocess.run(
                ["taskkill", "/f", "/im", f"{app_name}.exe"],
                capture_output=True
            )
            return f"✅ Closed: {app_name}"
        except Exception as e:
            return f"❌ Couldn't close {app_name}: {str(e)}"