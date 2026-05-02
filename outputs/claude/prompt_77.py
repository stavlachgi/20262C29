import subprocess
import sys

def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )
    
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    
    return result.returncode

def main():
    print("Shell Command Runner (type 'exit' to quit)")
    print("-" * 40)
    
    while True:
        try:
            command = input("$ ").strip()
            
            if not command:
                continue
            
            if command.lower() in ("exit", "quit"):
                break
            
            return_code = run_command(command)
            
            if return_code != 0:
                print(f"[exited with code {return_code}]", file=sys.stderr)
                
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            break

if __name__ == "__main__":
    main()
