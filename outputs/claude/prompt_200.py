import sys
import os
import platform
import traceback
import socket
import getpass


def get_system_info():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.architecture(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "cwd": os.getcwd(),
        "environment_variables": dict(os.environ),
        "path": sys.path,
    }


def format_detailed_error(exc: Exception) -> str:
    sys_info = get_system_info()
    tb = traceback.format_exc()

    lines = [
        "=" * 70,
        "DETAILED ERROR REPORT",
        "=" * 70,
        f"Error Type   : {type(exc).__name__}",
        f"Error Message: {exc}",
        "",
        "--- Traceback ---",
        tb,
        "--- System Information ---",
    ]

    for key, value in sys_info.items():
        if key == "environment_variables":
            lines.append(f"  {key}:")
            for k, v in value.items():
                lines.append(f"    {k} = {v}")
        elif key == "path":
            lines.append(f"  {key}:")
            for p in value:
                lines.append(f"    {p}")
        else:
            lines.append(f"  {key}: {value}")

    lines.append("=" * 70)
    return "\n".join(lines)


def risky_operation(value):
    if not isinstance(value, int):
        raise TypeError(f"Expected int, got {type(value).__name__}: {value!r}")
    if value == 0:
        raise ZeroDivisionError("Division by zero is not allowed")
    return 100 / value


def run(value):
    try:
        result = risky_operation(value)
        print(f"Result: {result}")
    except Exception as exc:
        print(format_detailed_error(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    test_cases = [0, "bad_input", 5]
    for tc in test_cases:
        print(f"\n>>> Testing with value: {tc!r}")
        run(tc)
