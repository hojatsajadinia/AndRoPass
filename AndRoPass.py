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
    
    try:
        args = parse_arguments()
        apk_file = validate_apk(args.apk)
        
        requirement_check = RequirementCheck()
        if not requirement_check.check():
            sys.exit(1)
        
        compiler = setup_compiler(requirement_check, args)
        if not process_apk(compiler):
            sys.exit(1)
            
        display_output_paths(compiler)
        
    except Exception as e:
        cp.pr("error", f"[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)

def validate_apk(apk_path: str) -> APKFile:
    apk_file = APKFile(apk_path)
    if not apk_file.exists():
        cp.pr("red", "[ERROR] APK file not found")
        sys.exit(1)
    if not apk_file.validate():
        cp.pr("red", "[ERROR] Invalid APK file")
        sys.exit(1)
    return apk_file

def setup_compiler(requirement_check: RequirementCheck, args) -> Compiler:
    return Compiler(
        requirement_check.apktool_path,
        requirement_check.uber_apk_signer_path,
        args.apk,
        args.apktool,
        args.apktool_path
    )

def process_apk(compiler: Compiler) -> bool:
    if not compiler.decompile():
        cp.pr("error", "[ERROR] Unable to decompile application")
        return False
        
    if not run_scanners(compiler):
        return False
        
    if not compiler.compile():
        cp.pr("error", "[ERROR] Unable to compile application")
        return False
        
    if not compiler.signer():
        cp.pr("error", "[ERROR] Unable to sign application")
        return False
        
    return True

def run_scanners(compiler: Compiler) -> bool:
    tasks = []
    with ThreadPoolExecutor() as executor:
        if compiler.status["decompile_with_res"]:
            tasks.append(executor.submit(Scanner().patterns_scanner, compiler.paths["decompile_with_res"]))
        if compiler.status["decompile_without_res"]:
            tasks.append(executor.submit(Scanner(False).patterns_scanner, compiler.paths["decompile_with_res"]))
        
        try:
            for future in as_completed(tasks):
                future.result()
            return True
        except Exception:
            return False

def display_output_paths(compiler: Compiler) -> None:
    for path_type in ["sign_with_res", "sign_without_res"]:
        if compiler.paths[path_type]:
            cp.pr("blue", f"[DONE] Application Out Path: {compiler.paths[path_type]}")

if __name__ == "__main__":
    main()
