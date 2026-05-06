import subprocess
import shlex
from typing import Tuple, Optional

def execute_command(user_input: str, timeout: int = 30) -> Tuple[int, str, str]:
    if not user_input or not user_input.strip():
        raise ValueError("Command input cannot be empty")
    
    try:
        args = shlex.split(user_input)
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return result.returncode, result.stdout, result.stderr
    
    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(
            cmd=user_input,
            timeout=timeout,
            output=e.stdout,
            stderr=e.stderr
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"Command not found: {args[0]}")

if __name__ == "__main__":
    try:
        return_code, stdout, stderr = execute_command("ls -la")
        print(f"Return code: {return_code}")
        print(f"Output:\n{stdout}")
        if stderr:
            print(f"Errors:\n{stderr}")
    
        return_code, stdout, stderr = execute_command("echo 'Hello, World!'")
        print(f"\nEcho output: {stdout.strip()}")
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
