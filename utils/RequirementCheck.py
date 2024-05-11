import os
import requests
from utils.ColorPrint import ColorPrint as cp
from subprocess import PIPE, Popen

class RequirementCheck:
    
    def __init__(self) -> None:
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.apktool_dir = os.path.join(self.base_path, "tools", "apktool")
        self.apktool_path = str()

        self.uber_apk_signer_dir = os.path.join(self.base_path, "tools", "uberApkSigner")
        self.uber_apk_signer_path = str()


    def check(self):
        cp.pr("info", "[INFO] Checking AndRoPass requirements")
        if not self.check_java_installed():
            cp.pr("error","[ERROR] No Java installed, Please install latest version of Java and try again.")
            return False
        else:
            cp.pr("info", f"[INFO] Java binary found: {self.get_java_version()}")
        
        if not self.check_apktool():
            cp.pr("error","[ERROR] Unable to find APKTool binary, check your internet connection or download APKTool Jar file manually and put in 'utils/tools/apktool' directory and try again")
            return False
        else:
            cp.pr("info", "[INFO] APKTool binary found")

        if not self.check_uber_Apk_signer():
            cp.pr("error","[ERROR] Unable to find Uber Apk Signer binary, check your internet connection or download Uber Apk Signer Jar file manually and put in 'utils/tools/uberApkSigner' directory and try again")
            return False
        else:
            cp.pr("info", "[INFO] Uber Apk Signer binary found")
        return True

    def check_apktool(self):
        res = False
        if not os.path.exists(self.apktool_dir):
            try:
                os.makedirs(self.apktool_dir)
            except Exception as e:
                cp.pr("error", f"[ERROR] Error making apktool directory: {e}")
        for file in os.listdir(self.apktool_dir):
            if file.endswith(".jar"):
                self.apktool_path = os.path.join(self.base_path,'tools','apktool', file)
                res = True
        try:
            url = "https://api.github.com/repos/iBotPeaches/Apktool/releases/latest"
            response = requests.get(url)
            download_url = response.json()["assets"][0]["browser_download_url"]
            download_name = response.json()["assets"][0]["name"]
            download_version = response.json()["name"]
            download_size = response.json()["assets"][0]["size"]
            if not os.path.exists(os.path.join(self.apktool_dir, download_name)) or os.path.getsize(os.path.join(self.apktool_dir, download_name)) != download_size :
                cp.pr("info", f"[INFO] Dowloading APKTool version: {download_version}")
                with open(os.path.join(self.apktool_dir, download_name), "wb") as file:
                    response = requests.get(download_url, stream=True)
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)      
                cp.pr("info", f"[INFO] APKTool {download_version} dowloaded")
                self.apktool_path = os.path.join(self.apktool_dir, download_name)
                return True
            
        except Exception as e:
            cp.pr("warn", "[WARN] Unable to get latest version of APKTool from Internet.")
            return res
        return res

    def check_uber_Apk_signer(self):
        res = False
        if not os.path.exists(self.uber_apk_signer_dir):
            try:
                os.makedirs(self.uber_apk_signer_dir)
            except Exception as e:
                cp.pr("error", f"[ERROR] Error making uberApkSigner directory: {e}")
        for file in os.listdir(self.uber_apk_signer_dir):
            if file.endswith(".jar"):
                self.uber_apk_signer_path = os.path.join(self.base_path,'tools','uberApkSigner', file)
                res = True
        try:
            url = "https://api.github.com/repos/patrickfav/uber-apk-signer/releases/latest"
            response = requests.get(url)
            download_url = response.json()["assets"][1]["browser_download_url"]
            download_name = response.json()["assets"][1]["name"]
            download_version = response.json()["name"]
            download_size = response.json()["assets"][1]["size"]
            if not os.path.exists(os.path.join(self.uber_apk_signer_dir, download_name)) or os.path.getsize(os.path.join(self.uber_apk_signer_dir, download_name)) != download_size :

                cp.pr("info", f"[INFO] Dowloading Uber APK Signer version: {download_version}")
                with open(os.path.join(self.uber_apk_signer_dir, download_name), "wb") as file:
                    response = requests.get(download_url, stream=True)
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)      
                cp.pr("info", f"[INFO] Uber APK Signer {download_version} dowloaded")
                self.uber_apk_signer_path = os.path.join(self.uber_apk_signer_dir, download_name)
                return True
            
        except Exception as e:
            cp.pr("warn", "[WARN] Unable to get latest version of Uber APK Signer from Internet.")
            return res
        return res

    def check_java_installed(self) -> bool:
        try:
            process = Popen(['java', '-version'],
                            stdout=PIPE,
                            stderr=PIPE)
            stdout, stderr = process.communicate()
        except FileNotFoundError as e:
            return print(e)
        try:
            self.java_version = str(stderr).split(
                r"\r\n")[0].split("version")[1].split(r"\n")[0]
            return True
        except IndexError as e:
            return False
        except TypeError as e:
            return False

    def get_java_version(self) -> str:
        try:
            return self.java_version
        except NameError as e:
            return None
