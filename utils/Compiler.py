
from subprocess import PIPE, Popen
from utils.ColorPrint import ColorPrint as cp
import uuid
import os
import sys

class Compiler:
    def __init__(self, apktool_path, uber_apk_signer_path, apk_path) -> None:
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.apktool_path = apktool_path
        self.apk_path = apk_path
        self.temp_dir = self.create_temp_dir()
        self.decompile_out_path_with_resource = str()
        self.decompile_out_path_without_resource = str()
        self.compile_out_path_with_resource = str()
        self.compile_out_path_without_resource = str()
        self.sign_out_path_with_resource = str()
        self.sign_out_path_without_resource = str()
        self.uber_apk_signer_path = uber_apk_signer_path

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
        decompile_out_path_with_resource = str()
        decompile_out_path_without_resource = str()
        
        # Generate random UUID4 for decompiling applcation with resource
        while True:
            uuidv4 = str(uuid.uuid4())
            decompile_out_path_with_resource = os.path.join(self.temp_dir, uuidv4)
            if not os.path.exists(decompile_out_path_with_resource):
                break
        
        # Generate random UUID4 for decompiling applcation without resource
        while True:
            uuidv4 = str(uuid.uuid4())
            decompile_out_path_without_resource = os.path.join(self.temp_dir, uuidv4)
            if not os.path.exists(decompile_out_path_without_resource):
                break

        # Decompile using APKTool with resource
        process = Popen(['java','-jar',self.apktool_path, 'd', '-f', self.apk_path, '-o' , decompile_out_path_with_resource ],
                            stdout=PIPE,
                            stderr=PIPE)
        stdout, stderr = process.communicate()
        if stderr != b'':
            cp.pr('error', f"[ERROR] {stderr.decode('utf-8')}")
        decompile_with_res_status = self.check_for_exception(stdout.decode('utf-8'))

        # Decompile using APKTool without resource
        process = Popen(['java','-jar',self.apktool_path, 'd', '-r', '-f', self.apk_path, '-o' , decompile_out_path_without_resource ],
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
            if decompile_with_res_status:
                self.decompile_out_path_with_resource = decompile_out_path_with_resource
            if decompile_without_res_status:
                self.decompile_out_path_without_resource = decompile_out_path_without_resource
            return True
        
    
    def compile(self):
        #TODO Change recompiled name due to same file names
        cp.pr("info", "[INFO] Compiling application")
        compile_with_res_status = True
        compile_without_res_status = True

        compile_out_path_with_resource =  os.path.join(os.path.dirname(self.apk_path), f"AndRoPass_WR_{os.path.basename(self.apk_path)}")
        compile_out_path_without_resource =  os.path.join(os.path.dirname(self.apk_path), f"AndRoPass_WOR_{os.path.basename(self.apk_path)}")

        #TODO Compile with use aapt2 flag
        # APK compiling with resource
        if self.decompile_out_path_with_resource != '':
            process = Popen(['java','-jar',self.apktool_path, 'b', self.decompile_out_path_with_resource, '-o', compile_out_path_with_resource],
                            stdout=PIPE,
                            stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr != b'':
                cp.pr('error', f"[ERROR] {stderr.decode('utf-8')}")
                compile_with_res_status = False
            compile_with_res_status = compile_with_res_status and self.check_for_exception(stdout.decode('utf-8'))

        # APK compiling without resource
        if self.decompile_out_path_without_resource != '':
            process = Popen(['java','-jar',self.apktool_path, 'b', self.decompile_out_path_without_resource, '-o', compile_out_path_without_resource ],
                            stdout=PIPE,
                            stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr != b'':
                cp.pr('error', f"[ERROR] {stderr.decode('utf-8')}")
                compile_without_res_status = False
            compile_without_res_status = compile_without_res_status and self.check_for_exception(stdout.decode('utf-8'))

            if (compile_with_res_status or compile_without_res_status) != True:
                # TODO Try multiple apktool versions to fix compilation errors
                cp.pr("error", "[ERROR] Unable to decompile applicaiton")
                sys.exit(1)
            else:
                if compile_with_res_status:
                    self.compile_out_path_with_resource = compile_out_path_with_resource
                if compile_without_res_status:
                    self.compile_out_path_without_resource = compile_out_path_without_resource
                return True
            
    def signer(self):
        cp.pr("info", "[INFO] Signing application")

        # APK signing with resource
        if self.compile_out_path_with_resource != '':
            process = Popen(['java','-jar',self.uber_apk_signer_path, '--apks', self.compile_out_path_with_resource, '-o', os.path.dirname(self.apk_path)],
                            stdout=PIPE,
                            stderr=PIPE)
            stdout, stderr1 = process.communicate()
            self.sign_out_path_with_resource = self.compile_out_path_with_resource.replace(".apk", "-aligned-debugSigned.apk")
            
        # APK signing without resource
        if self.compile_out_path_without_resource != '':
            process = Popen(['java','-jar',self.uber_apk_signer_path, '--apks', self.compile_out_path_without_resource, '-o', os.path.dirname(self.apk_path)],
                            stdout=PIPE,
                            stderr=PIPE)
            stdout, stderr2 = process.communicate()
            self.sign_out_path_without_resource = self.compile_out_path_without_resource.replace(".apk", "-aligned-debugSigned.apk")

        #TODO check for sign errors
        return True
    
    def check_for_exception(self,apktool_output) -> bool:
        # TODO check all apktool error
        for line in apktool_output.split("\n"):
            if ":" in line:
                if line.split(":")[0][-1] != "I":
                    return False
        return True