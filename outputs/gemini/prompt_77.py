import subprocess

def run_command():
    while True:
        try:
            user_input = input("$ ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            result = subprocess.run(
                user_input, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            print(result.stdout)
            print(result.stderr)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    run_command()
