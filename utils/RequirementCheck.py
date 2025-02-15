import os
import requests
from subprocess import PIPE, Popen, TimeoutError
from pathlib import Path
from typing import Optional, Tuple
from utils.ColorPrint import ColorPrint as cp

class RequirementCheck:
    """Class to check and validate all requirements for the application."""

    def __init__(self) -> None:
        self.base_path = Path(__file__).parent
        self.tools_dir = self.base_path / "tools"
        self.paths = {
            "apktool": self.tools_dir / "apktool",
            "uber_apk_signer": self.tools_dir / "uberApkSigner"
        }
        self.tool_paths = {
            "apktool": "",
            "uber_apk_signer": ""
        }
        self.java_version = ""

    def check(self) -> bool:
        """Perform all requirement checks."""
        cp.pr("info", "[INFO] Checking AndRoPass requirements")
        
        if not self._check_java():
            return False
            
        tools_status = all([
            self._check_tool("apktool", "APKTool"),
            self._check_tool("uber_apk_signer", "Uber APK Signer")
        ])
        
        return tools_status

    def _check_java(self) -> bool:
        """Check Java installation and version."""
        if not self._get_java_version():
            cp.pr("error", "[ERROR] Java not installed. Please install the latest version.")
            return False
            
        cp.pr("info", f"[INFO] Java binary found: {self.java_version}")
        return True

    def _get_java_version(self) -> bool:
        """Get Java version string."""
        try:
            process = Popen(['java', '-version'], stdout=PIPE, stderr=PIPE)
            _, stderr = process.communicate(timeout=10)
            version_output = stderr.decode('utf-8', errors='ignore')
            
            if 'version' in version_output:
                self.java_version = version_output.split('\n')[0]
                return True
        except (FileNotFoundError, TimeoutError, Exception):
            pass
        return False

    def _check_tool(self, tool_key: str, tool_name: str) -> bool:
        """Check if a required tool is available and download if necessary."""
        tool_dir = self.paths[tool_key]
        tool_dir.mkdir(parents=True, exist_ok=True)
        
        jar_path = self._find_jar_file(tool_dir)
        if jar_path:
            self.tool_paths[tool_key] = str(jar_path)
            cp.pr("info", f"[INFO] {tool_name} binary found")
            return True
            
        return self._download_tool(tool_key, tool_name)

    def _find_jar_file(self, directory: Path) -> Optional[Path]:
        """Find .jar file in the specified directory."""
        try:
            return next(directory.glob("*.jar"), None)
        except Exception:
            return None

    def _download_tool(self, tool_key: str, tool_name: str) -> bool:
        """Download the specified tool."""
        repo_map = {
            "apktool": "iBotPeaches/Apktool",
            "uber_apk_signer": "patrickfav/uber-apk-signer"
        }
        
        try:
            success = self._download_latest_release(
                repo_map[tool_key],
                self.paths[tool_key],
                tool_key
            )
            if success:
                cp.pr("info", f"[INFO] {tool_name} downloaded successfully")
                return True
                
        except Exception as e:
            cp.pr("error", f"[ERROR] Failed to download {tool_name}: {e}")
            
        return False

    def _download_latest_release(self, repo: str, download_dir: Path, tool_key: str) -> bool:
        """Download the latest release of a tool from GitHub."""
        response = requests.get(f"https://api.github.com/repos/{repo}/releases/latest")
        response.raise_for_status()
        
        asset = response.json()["assets"][0]
        download_url = asset["browser_download_url"]
        download_path = download_dir / asset["name"]
        
        if not download_path.exists() or download_path.stat().st_size != asset["size"]:
            cp.pr("info", f"[INFO] Downloading {repo.split('/')[1]} version: {response.json()['name']}")
            
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
        self.tool_paths[tool_key] = str(download_path)
        return True
