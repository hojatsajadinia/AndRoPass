
from subprocess import PIPE, Popen
from utils.ColorPrint import ColorPrint as cp
import uuid
import os
import sys

class Compiler:
    def __init__(self, apktool_path, apk_path) -> None:
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.apktool_path = apktool_path
        self.apk_path = apk_path
        self.temp_dir = self.create_temp_dir()

    def create_temp_dir(self):
        try:
            if not os.path.exists(os.path.join(self.base_path, "temp")):
                os.makedirs(os.path.join(self.base_path, "temp"))
            return os.path.join(self.base_path, "temp")
        except Exception as e:
            cp.pr("error", f"[ERROR] Unable to create temp directory, {e}")
            sys.exit(1)

    def decompile(self):
        cp.pr("info", "[INFO] Decompiling applicaiton")
        out_path_with_resource = str()
        out_path_without_resource = str()
        while True:
            uuidv4 = str(uuid.uuid4())
            out_path_with_resource = os.path.join(self.temp_dir, uuidv4)
            if not os.path.exists(out_path_with_resource):
                break
        while True:
            uuidv4 = str(uuid.uuid4())
            out_path_without_resource = os.path.join(self.temp_dir, uuidv4)
            if not os.path.exists(out_path_without_resource):
                break
        process = Popen(['java','-jar',self.apktool_path, 'd', '-f', self.apk_path, '-o' , out_path_with_resource ],
                            stdout=PIPE,
                            stderr=PIPE)
        stdout, stderr = process.communicate()
        if stderr != b'':
            cp.pr('error', f"[ERROR] {stderr.decode('utf-8')}")
        decompile_with_res_status = self.check_for_exception(stdout.decode('utf-8'))

        process = Popen(['java','-jar',self.apktool_path, 'd', '-r', '-f', self.apk_path, '-o' , out_path_without_resource ],
                            stdout=PIPE,
                            stderr=PIPE)
        stdout, stderr = process.communicate()
        if stderr != b'':
            cp.pr('error', f"[ERROR] {stderr.decode('utf-8')}")
        decompile_without_res_status = self.check_for_exception(stdout.decode('utf-8'))

        if (decompile_with_res_status or decompile_without_res_status) != True:
            # TODO Try multiple apktool versions to fix decompilation errors
            cp.pr("error", "[ERROR] Unable to decompile applicaiton")
            sys.exit(1)
        else:
            return out_path_with_resource, out_path_without_resource

    
    def check_for_exception(self,apktool_output) -> bool:
        # TODO check all apktool error
        for line in apktool_output.split("\n"):
            if ":" in line:
                if line.split(":")[0][-1] != "I":
                    return False
        return True