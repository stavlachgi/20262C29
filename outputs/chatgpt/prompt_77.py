import subprocess
import shlex

while True:
    try:
        cmd = input()
        if not cmd:
            continue
        args = shlex.split(cmd)
        result = subprocess.run(args, capture_output=True, text=True)
        print(result.stdout, end="")
        print(result.stderr, end="")
    except EOFError:
        break
    except Exception as e:
        print(str(e))
