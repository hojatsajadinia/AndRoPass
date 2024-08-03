import os
import sys
import uuid
from subprocess import PIPE, Popen
from utils.ColorPrint import ColorPrint as cp

class Compiler:
    def __init__(self, apktool_path, uber_apk_signer_path, apk_path, use_system_apktool, system_apktool_path) -> None:
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.apktool_path = apktool_path
        self.apk_path = apk_path
        self.temp_dir = self.create_temp_dir()

        self.paths = {
            "decompile_with_res": "",
            "decompile_without_res": "",
            "compile_with_res": "",
            "compile_without_res": "",
            "sign_with_res": "",
            "sign_without_res": ""
        }

        self.status = {
            "decompile_with_res": True,
            "decompile_without_res": True,
            "compile_with_res": True,
            "compile_without_res": True
        }

        self.uber_apk_signer_path = uber_apk_signer_path
        self.apktool_command = self.get_apktool_command(use_system_apktool, system_apktool_path)

    def create_temp_dir(self):
        temp_dir = os.path.join(self.base_path, "temp")
        try:
            os.makedirs(temp_dir, exist_ok=True)
            return temp_dir
        except Exception as e:
            cp.pr("error", f"[ERROR] Unable to create temp directory, {e}")
            sys.exit(1)

    def get_apktool_command(self, use_system_apktool, system_apktool_path):
        if use_system_apktool:
            return ['apktool']
        elif system_apktool_path:
            return ['java', '-jar', system_apktool_path]
        else:
            return ['java', '-jar', self.apktool_path]

    def generate_uuid_path(self, base_dir):
        while True:
            path = os.path.join(base_dir, str(uuid.uuid4()))
            if not os.path.exists(path):
                return path

    def run_process(self, command):
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8', errors='ignore'), stderr.decode('utf-8', errors='ignore')

    def check_for_exception(self, apktool_output):
        return all(line.split(":")[0][-1] == "I" for line in apktool_output.split("\n") if ":" in line)

    def decompile(self):
        cp.pr("info", "[INFO] Decompiling application")
        self.paths["decompile_with_res"] = self.generate_uuid_path(self.temp_dir)
        self.paths["decompile_without_res"] = self.generate_uuid_path(self.temp_dir)

        commands = [
            (self.apktool_command + ['d', '-f', self.apk_path, '-o', self.paths["decompile_with_res"]], "decompile_with_res"),
            (self.apktool_command + ['d', '-r', '-f', self.apk_path, '-o', self.paths["decompile_without_res"]], "decompile_without_res")
        ]

        for command, key in commands:
            stdout, stderr = self.run_process(command)
            if stderr:
                self.status[key] = False
            self.status[key] = self.status[key] and self.check_for_exception(stdout)

        if not (self.status["decompile_with_res"] or self.status["decompile_without_res"]):
            cp.pr("error", "[ERROR] Unable to decompile application")
            sys.exit(1)
        return True

    def compile(self):
        cp.pr("info", "[INFO] Compiling application")
        apk_name = os.path.basename(self.apk_path)
        apk_dir = os.path.dirname(self.apk_path)
        self.paths["compile_with_res"] = os.path.join(apk_dir, f"AndRoPass_WR_{apk_name}")
        self.paths["compile_without_res"] = os.path.join(apk_dir, f"AndRoPass_WOR_{apk_name}")

        commands = []

        if self.status["decompile_with_res"]:
            commands.append((self.apktool_command + ['b', self.paths["decompile_with_res"], '-o', self.paths["compile_with_res"]], "compile_with_res"))
        if self.status["decompile_without_res"]:
            commands.append((self.apktool_command + ['b', self.paths["decompile_without_res"], '-o', self.paths["compile_without_res"]], "compile_without_res"))

        for command, key in commands:
            if self.status[key.replace("compile", "decompile")]:
                stdout, stderr = self.run_process(command)
                if stderr:
                    self.status[key] = False
                self.status[key] = self.status[key] and self.check_for_exception(stdout)

        if not (self.status["compile_with_res"] or self.status["compile_without_res"]):
            cp.pr("error", "[ERROR] Unable to compile application")
            sys.exit(1)
        return True

    def signer(self):
        cp.pr("info", "[INFO] Signing application")
        commands = []

        if self.status["compile_with_res"]:
            commands.append((['java', '-jar', self.uber_apk_signer_path, '--apks', self.paths["compile_with_res"], '-o', os.path.dirname(self.apk_path)], "sign_with_res"))
        if self.status["compile_without_res"]:
            commands.append((['java', '-jar', self.uber_apk_signer_path, '--apks', self.paths["compile_without_res"], '-o', os.path.dirname(self.apk_path)], "sign_without_res"))

        for command, key in commands:
            if self.paths[key.replace("sign", "compile")]:
                self.run_process(command)
                self.paths[key] = self.paths[key.replace("sign", "compile")].replace(".apk", "-aligned-debugSigned.apk")

        return True
