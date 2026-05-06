import subprocess
import sys


def run_command(command: str) -> None:
    if not command.strip():
        print("Error: Empty command provided")
        return
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"\nCommand failed with return code: {result.returncode}")
        else:
            print("\nCommand executed successfully")
            
    except subprocess.TimeoutExpired:
        print("Error: Command timed out after 30 seconds")
    except Exception as e:
        print(f"Error executing command: {e}")


def main() -> None:
    print("Shell Command Runner")
    print("=" * 50)
    print("Enter shell commands to execute (type 'exit' to quit)")
    print("=" * 50)
    
    while True:
        try:
            command = input("\n$ ").strip()
            
            if command.lower() in ("exit", "quit"):
                print("Exiting...")
                sys.exit(0)
            
            if command:
                run_command(command)
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            sys.exit(0)
        except EOFError:
            print("\nExiting...")
            sys.exit(0)


if __name__ == "__main__":
    main()
