import os
import zipfile
from pathlib import Path
from typing import Optional

class APKFile:
    """Class to handle APK file operations and validation."""
    
    def __init__(self, apk_path: str) -> None:
        self.apk_path = self._resolve_path(apk_path)
    
    def _resolve_path(self, apk_path: str) -> str:
        """Resolve the APK path relative to the base directory if necessary."""
        if os.path.exists(apk_path):
            return apk_path
            
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, apk_path)
        return full_path

    def exists(self) -> bool:
        """Check if the APK file exists."""
        return os.path.exists(self.apk_path)

    def validate(self) -> bool:
        """
        Validate that the file is a valid APK by checking for AndroidManifest.xml.
        """
        if not self.exists():
            return False
            
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
                return 'AndroidManifest.xml' in zip_ref.namelist()
        except zipfile.BadZipFile:
            return False
        except Exception:
            return False
            
    def get_size(self) -> Optional[int]:
        """Get the size of the APK file in bytes."""
        try:
            return os.path.getsize(self.apk_path)
        except OSError:
            return None
