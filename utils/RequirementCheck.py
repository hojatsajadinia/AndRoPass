import os
import requests
from subprocess import PIPE, Popen
from utils.ColorPrint import ColorPrint as cp

class RequirementCheck:
    def __init__(self) -> None:
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.tools_dir = os.path.join(self.base_path, "tools")
        self.apktool_dir = os.path.join(self.tools_dir, "apktool")
        self.uber_apk_signer_dir = os.path.join(self.tools_dir, "uberApkSigner")
        self.apktool_path = ""
        self.uber_apk_signer_path = ""
        self.java_version = ""

    def check(self) -> bool:
        cp.pr("info", "[INFO] Checking AndRoPass requirements")
        if not self.check_java_installed():
            cp.pr("error", "[ERROR] No Java installed, Please install the latest version of Java and try again.")
            return False
        cp.pr("info", f"[INFO] Java binary found: {self.get_java_version()}")

        if not self.check_apktool():
            cp.pr("error", "[ERROR] Unable to find APKTool binary. Please check your internet connection or download the APKTool jar file manually and place it in the 'tools/apktool' directory.")
            return False
        cp.pr("info", "[INFO] APKTool binary found")

        if not self.check_uber_apk_signer():
            cp.pr("error", "[ERROR] Unable to find Uber APK Signer binary. Please check your internet connection or download the Uber APK Signer jar file manually and place it in the 'tools/uberApkSigner' directory.")
            return False
        cp.pr("info", "[INFO] Uber APK Signer binary found")

        return True

    def check_apktool(self) -> bool:
        self.create_directory_if_not_exists(self.apktool_dir)
        self.apktool_path = self.find_jar_file(self.apktool_dir)
        
        if not self.apktool_path:
            return self.download_latest_release(
                repo="iBotPeaches/Apktool",
                download_dir=self.apktool_dir,
                path_attr="apktool_path"
            )
        return True

    def check_uber_apk_signer(self) -> bool:
        self.create_directory_if_not_exists(self.uber_apk_signer_dir)
        self.uber_apk_signer_path = self.find_jar_file(self.uber_apk_signer_dir)
        
        if not self.uber_apk_signer_path:
            return self.download_latest_release(
                repo="patrickfav/uber-apk-signer",
                download_dir=self.uber_apk_signer_dir,
                path_attr="uber_apk_signer_path"
            )
        return True

    def create_directory_if_not_exists(self, directory: str) -> None:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                cp.pr("error", f"[ERROR] Error creating directory {directory}: {e}")

    def find_jar_file(self, directory: str) -> str:
        for file in os.listdir(directory):
            if file.endswith(".jar"):
                return os.path.join(directory, file)
        return ""

    def download_latest_release(self, repo: str, download_dir: str, path_attr: str) -> bool:
        try:
            url = f"https://api.github.com/repos/{repo}/releases/latest"
            response = requests.get(url)
            response.raise_for_status()
            asset = response.json()["assets"][0]
            download_url = asset["browser_download_url"]
            download_name = asset["name"]
            download_size = asset["size"]
            download_path = os.path.join(download_dir, download_name)

            if not os.path.exists(download_path) or os.path.getsize(download_path) != download_size:
                cp.pr("info", f"[INFO] Downloading {repo.split('/')[1]} version: {response.json()['name']}")
                with open(download_path, "wb") as file:
                    response = requests.get(download_url, stream=True)
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                cp.pr("info", f"[INFO] {repo.split('/')[1]} downloaded")
                setattr(self, path_attr, download_path)
                return True
        except Exception as e:
            cp.pr("warn", f"[WARN] Unable to download the latest version of {repo.split('/')[1]}: {e}")
            return False
        return True

    def check_java_installed(self) -> bool:
        try:
            process = Popen(['java', '-version'], stdout=PIPE, stderr=PIPE)
            _, stderr = process.communicate()
            self.java_version = str(stderr).split(r"\r\n")[0].split("version")[1].strip()
            return True
        except (FileNotFoundError, IndexError, TypeError):
            return False

    def get_java_version(self) -> str:
        return self.java_version
