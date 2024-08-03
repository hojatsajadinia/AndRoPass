import os
import zipfile

class APKFile:
    def __init__(self, apk_path: str) -> None:
        self.apk_path = apk_path
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def exists(self) -> bool:
        return os.path.exists(self.apk_path) or os.path.exists(os.path.join(self.base_dir, self.apk_path))

    def validate(self) -> bool:
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
                return 'AndroidManifest.xml' in zip_ref.namelist()
        except zipfile.BadZipFile:
            return False
