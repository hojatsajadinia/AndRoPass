import os
from pathlib import Path
import regex as re
from utils.Const import Const
from utils.ColorPrint import ColorPrint as cp

class Scanner:
    def __init__(self, scan_with_resource: bool = True) -> None:
        self.pattern_counts = {
            'root': 0,
            'emulator': 0
        }
        self.scan_with_resource = scan_with_resource

    def patterns_scanner(self, directory_path: str) -> bool:
        self.scan_directory(directory_path)
        self.log_detection_results()
        
        if any(self.pattern_counts.values()):
            return True
        cp.pr("error", "[ERROR] Unable to scan the application")
        return False

    def scan_directory(self, directory_path: str) -> None:
        try:
            for root, _, files in os.walk(directory_path):
                for file_name in files:
                    if file_name.endswith(".smali"):
                        file_path = Path(root) / file_name
                        self.process_file(file_path)
        except Exception as e:
            cp.pr("error", f"[ERROR] An error occurred while scanning the directory: {e}")

    def process_file(self, file_path: Path) -> None:
        try:
            with open(file_path, 'r+') as file:
                content = file.read()
                modified_content = self.bypass_detections(content)
                
                if modified_content != content:
                    file.seek(0)
                    file.write(modified_content)
                    file.truncate()

        except Exception as e:
            cp.pr("error", f"[ERROR] An error occurred while processing {file_path}: {e}")

    def bypass_detections(self, content: str) -> str:
        patterns = {
            'root': Const.all_root_values,
            'emulator': Const.all_emulator_values
        }
        
        for detection_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                count = content.count(pattern)
                self.pattern_counts[detection_type] += count
                if count > 0:
                    content = re.sub(pattern, f"{pattern[0]}X{pattern[2:]}", content)
        
        return content

    def log_detection_results(self) -> None:
        resource_suffix = "" if self.scan_with_resource else " - without Resource"
        
        for detection_type, count in self.pattern_counts.items():
            if count > 0:
                cp.pr("info", f"[INFO] {count} {detection_type.title()} Detection Pattern(s) Detected{resource_suffix}.")
