import sys
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.ColorPrint import ColorPrint as cp
from utils.APKFile import APKFile
from utils.RequirementCheck import RequirementCheck
from utils.Compiler import Compiler
from utils.Scanner import Scanner

DES = """
 █████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ██████╗  █████╗ ███████╗███████╗
██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
███████║██╔██╗ ██║██║  ██║██████╔╝██║   ██║██████╔╝███████║███████╗███████╗
██╔══██║██║╚██╗██║██║  ██║██╔══██╗██║   ██║██╔═══╝ ██╔══██║╚════██║╚════██║
██║  ██║██║ ╚████║██████╔╝██║  ██║╚██████╔╝██║     ██║  ██║███████║███████║
╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
https://github.com/hojatsajadinia/AndRoPass                 
"""

def parse_arguments():
    parser = ArgumentParser(prog='AndRoPass', description='Android Root and Emulator Detection Bypass Tool')
    parser.add_argument('--apk', '-a', type=str, required=True, help='APK full path')
    parser.add_argument('--apktool', required=False, action='store_true', help="Use the apktool command from your system's PATH.")
    parser.add_argument('--apktool-path', type=str, required=False, help="Set your desired apktool path in .jar format.")
    return parser.parse_args()

def main():
    cp.pr('blue', DES)

    args = parse_arguments()
    apk_file_path = args.apk
    use_system_apktool = args.apktool
    system_apktool_path = args.apktool_path

    apk_file = APKFile(apk_file_path)
    if not apk_file.exists():
        cp.pr("red", "[ERROR] APK file not found")
        sys.exit(1)
    if not apk_file.validate():
        cp.pr("red", "[ERROR] Invalid APK file")
        sys.exit(1)
    
    requirement_check = RequirementCheck()
    if not requirement_check.check():
        sys.exit(1)
    
    compiler = Compiler(requirement_check.apktool_path, requirement_check.uber_apk_signer_path, apk_file_path, use_system_apktool, system_apktool_path)
    if not compiler.decompile():
        cp.pr("error", "[ERROR] Unable to decompile application")
        sys.exit(1)

    tasks = []
    with ThreadPoolExecutor() as executor:
        if compiler.status["decompile_with_res"]:
            scanner_with_res = Scanner()
            tasks.append(executor.submit(scanner_with_res.patterns_scanner, compiler.paths["decompile_with_res"]))
        
        if compiler.status["decompile_without_res"]:
            scanner_without_res = Scanner(False)
            tasks.append(executor.submit(scanner_without_res.patterns_scanner, compiler.paths["decompile_with_res"]))
        
        for future in as_completed(tasks):
            future.result()  # Will raise an exception if the scan task failed

    if not compiler.compile():
        cp.pr("error", "[ERROR] Unable to compile application")
        sys.exit(1)
    
    if not compiler.signer():
        cp.pr("error", "[ERROR] Unable to sign application")
        sys.exit(1)
    
    if compiler.paths["sign_with_res"]:
        cp.pr("blue", f"[DONE] Application Out Path: {compiler.paths['sign_with_res']}")
    if compiler.paths["sign_without_res"]:
        cp.pr("blue", f"[DONE] Application Out Path: {compiler.paths['sign_without_res']}")

if __name__ == "__main__":
    main()
