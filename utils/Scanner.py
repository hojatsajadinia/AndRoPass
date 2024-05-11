import os
import re
from utils.Const import Const
from utils.ColorPrint import ColorPrint as cp

class Scanner:
    def __init__(self) -> None:
        self.root_pattern_count = 0
        self.emulator_pattern_count = 0
    
    def patterns_scanner(self,directory_path):
        self.patterns_scanner_implementation(directory_path)
        
        if self.root_pattern_count:
            cp.pr("info", f"[INFO] {self.root_pattern_count} Root Detection Pattern/s Detected.")
        if self.emulator_pattern_count:
            cp.pr("info", f"[INFO] {self.emulator_pattern_count} Emulator Detection Pattern/s Detected.")

        
        if self.root_pattern_count or self.emulator_pattern_count:
            return True
        else:
            cp.pr("error", "[ERROR] Unable to scann the application")
            return False
      
    def patterns_scanner_implementation(self,directory_path):
        try:
            for root, _, files in os.walk(directory_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if file_path.endswith(".smali"):
                        with open(file_path, 'r') as file:
                            file_content = file.read()

                            # Root Detection
                            file_content = self.root_detection_bypass(file_content)

                            # Emulator Detection
                            file_content = self.emulator_detection_bypass(file_content)

                        with open(file_path, 'w') as file:
                            file.write(file_content)
        except Exception as e:
            pass
    
    def root_detection_bypass(self, file_content):
        for search_str in Const.all_root_values:
            self.root_pattern_count += file_content.count(search_str)
            return re.sub(search_str, f"{search_str[0]}X{search_str[2:]}", file_content)
    
    def emulator_detection_bypass(self, file_content):
        for search_str in Const.all_emulator_values:
            self.emulator_pattern_count += file_content.count(search_str)
            return re.sub(search_str, f"{search_str[0]}X{search_str[2:]}", file_content)



