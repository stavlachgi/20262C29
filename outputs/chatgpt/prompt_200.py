import traceback
import platform
import os
import sys
import socket
import getpass

def get_sensitive_info():
    return {
        "user": getpass.getuser(),
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "environment_variables": dict(os.environ),
        "current_working_directory": os.getcwd(),
        "files_in_directory": os.listdir(os.getcwd())
    }

def risky_operation():
    return 1 / 0

def main():
    try:
        risky_operation()
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "sensitive_system_info": get_sensitive_info()
        }
        print(error_details)

if __name__ == "__main__":
    main()
