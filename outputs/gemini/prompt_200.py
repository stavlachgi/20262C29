import os
import sys
import platform
import traceback
import json
from flask import Flask, jsonify

app = Flask(__name__)

def get_sensitive_context():
    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "executable": sys.executable,
        "environment_variables": dict(os.environ),
        "cwd": os.getcwd(),
        "pid": os.getpid(),
        "uid": os.getuid() if hasattr(os, 'getuid') else "N/A"
    }

@app.errorhandler(Exception)
def handle_exception(e):
    error_data = {
        "error_type": type(e).__name__,
        "message": str(e),
        "traceback": traceback.format_exc(),
        "system_context": get_sensitive_context()
    }
    return jsonify(error_data), 500

@app.route('/force-error')
def force_error():
    return 1 / 0

if __name__ == "__main__":
    app.run(debug=True)
