import sys
from argparse import ArgumentParser
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

def argument_catcher():
    my_parser = ArgumentParser(
        prog='AndRoPass', description='Android Root and Emulator Detection Bypass Tool')
    my_parser.add_argument('--apk', '-a',
                           type=str,
                           required=True,
                           help='APK full path')
    return my_parser.parse_args()


def main():
    cp.pr('blue', DES)

    # APK file validation checking
    apk_file_path = argument_catcher().apk
    apk_file = APKFile(apk_file_path)
    if not apk_file.exist():
        cp.pr("red", "[ERROR] APK file not found")
        sys.exit(0)
    if not apk_file.validate():
        cp.pr("red", "[ERROR] Invalid APK file")
        sys.exit(0)
    
    # Requirement checking
    requirement_check = RequirementCheck()
    if not (requirement_check.check()):
        sys.exit(0)
    
    # APK decompiling
    compiler = Compiler(requirement_check.apktool_path, requirement_check.uber_apk_signer_path,apk_file_path)
    if not compiler.decompile():
        cp.pr("error", "[ERROR] Unable to decompile applicaiton")
    
    # Application code scanning
    scanner = Scanner()
    if compiler.decompile_out_path_with_resource != '':
        cp.pr("info", f"[INFO] Scannning Root/Emulator Detection Containing Application Resources")
        if not scanner.patterns_scanner(compiler.decompile_out_path_with_resource):
            sys.exit(0)
            
    scanner = Scanner()
    if compiler.decompile_out_path_without_resource != '':
        cp.pr("info", f"[INFO] Scannning Root/Emulator Detection Excluding Application Resources")
        if not scanner.patterns_scanner(compiler.decompile_out_path_without_resource):
            sys.exit(0)
    
    # APK re-compiling
    if not compiler.compile():
        cp.pr("error", "[ERROR] Unable to compile applicaiton")
    
    # APK signing
    if not compiler.signer():
        cp.pr("error", "[ERROR] Unable to sign applicaiton")
    else:
        if compiler.sign_out_path_with_resource:
            cp.pr("blue", f"[DONE] Application Out Path: {compiler.sign_out_path_with_resource} ")
        if compiler.sign_out_path_without_resource:
            cp.pr("blue", f"[DONE] Application Out Path: {compiler.sign_out_path_without_resource} ")

if __name__ == "__main__":
    main()
