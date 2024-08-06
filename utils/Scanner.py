import os
from pathlib import Path
import regex as re
from utils.Const import Const
from utils.ColorPrint import ColorPrint as cp

class Scanner:
    def __init__(self, scan_with_resource: bool = True) -> None:
        self.root_pattern_count = 0
        self.emulator_pattern_count = 0
        self.scan_with_resource = scan_with_resource

    def patterns_scanner(self, directory_path: str) -> bool:
        self.scan_directory(directory_path)
        
        self.log_detection_results()

        if self.root_pattern_count or self.emulator_pattern_count:
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
                file_content = file.read()

                file_content = self.root_detection_bypass(file_content)
                file_content = self.emulator_detection_bypass(file_content)

                file.seek(0)
                file.write(file_content)
                file.truncate()

        except Exception as e:
            cp.pr("error", f"[ERROR] An error occurred while processing the file {file_path}: {e}")


    def root_detection_bypass(self, file_content: str) -> str:
        for search_str in Const.all_root_values:
            self.root_pattern_count += file_content.count(search_str)
            file_content = re.sub(search_str, f"{search_str[0]}X{search_str[2:]}", file_content)
        return file_content

    def emulator_detection_bypass(self, file_content: str) -> str:
        for search_str in Const.all_emulator_values:
            self.emulator_pattern_count += file_content.count(search_str)
            file_content = re.sub(search_str, f"{search_str[0]}X{search_str[2:]}", file_content)
        return file_content

    def log_detection_results(self) -> None:
        resource_suffix = "" if self.scan_with_resource else " - without Resource"
        if self.root_pattern_count:
            cp.pr("info", f"[INFO] {self.root_pattern_count} Root Detection Pattern(s) Detected{resource_suffix}.")
        if self.emulator_pattern_count:
            cp.pr("info", f"[INFO] {self.emulator_pattern_count} Emulator Detection Pattern(s) Detected{resource_suffix}.")
