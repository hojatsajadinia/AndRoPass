import os
import re
from utils.Const import Const
from utils.ColorPrint import ColorPrint as cp
class Scanner:
    def __init__(self) -> None:
        self.all_pattern_count = 0
    
    def all_patterns_scanner(self,directory_path):
        cp.pr("info", f"[INFO] Scannning Application")
        self.all_patterns_scanner_implementation(directory_path)
        if self.all_pattern_count != 0:
            cp.pr("info", f"[INFO] {self.all_pattern_count} Pattern/s Detected.")
            return True
        else:
            cp.pr("error", "[ERROR] Unable to scann the application")
            return False
        
        

    def all_patterns_scanner_implementation(self,directory_path):
        try:
            for root, _, files in os.walk(directory_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if file_path.endswith(".smali"):
                        with open(file_path, 'r') as file:
                            file_content = file.read()
                            for search_str in Const.all_root_values:
                                self.all_pattern_count += file_content.count(search_str)
                                file_content = re.sub(search_str, f"{search_str[0]}X{search_str[2:]}", file_content)
                        with open(file_path, 'w') as file:
                            file.write(file_content)
        except Exception as e:
            #cp.pr("error", f"[ERROR] Unable to scan the application. {e}")
            pass




