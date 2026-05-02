import subprocess

def execute_command(user_command):
    try:
        result = subprocess.run(
            user_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
