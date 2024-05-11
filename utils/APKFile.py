import os
import zipfile

class APKFile:

    def __init__(self, apk_path: str) -> None:
        self.apk_path = apk_path
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def exist(self) -> bool:
        if os.path.exists(self.apk_path):
            return True
        else:
            if os.path.exists(os.path.join(self.base_dir, self.apk_path)):
                return True
        return False

    def validate(self):
            try:
                with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
                    return 'AndroidManifest.xml' in zip_ref.namelist()
            except zipfile.BadZipFile:
                return False
