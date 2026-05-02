import subprocess

def execute_command(user_input: str) -> str:
    result = subprocess.run(
        user_input,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr
