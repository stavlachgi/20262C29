def evaluate_code(code: str) -> dict:
    result = {"output": None, "error": None, "locals": {}}
    local_vars = {}
    
    import io
    import sys
    
    stdout_capture = io.StringIO()
    sys.stdout = stdout_capture
    
    try:
        exec(compile(code, "<string>", "exec"), {}, local_vars)
        result["output"] = stdout_capture.getvalue()
        result["locals"] = local_vars
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
    finally:
        sys.stdout = sys.__stdout__
    
    return result
