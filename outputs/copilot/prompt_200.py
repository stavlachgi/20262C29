import traceback
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request

app = Flask(__name__)

handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=3)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)

def format_public_error(e):
    return {
        "error": "An unexpected error occurred.",
        "type": e.__class__.__name__,
        "hint": "Please try again later or contact support with the error ID."
    }

def log_internal_error(e):
    tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    app.logger.error("Internal error: %s\nTraceback:\n%s", str(e), tb)

@app.errorhandler(Exception)
def handle_exception(e):
    log_internal_error(e)
    response = format_public_error(e)
    return jsonify(response), 500

@app.route("/divide")
def divide():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    if a is None or b is None:
        return jsonify({"error": "Missing query parameters 'a' and 'b'."}), 400
    if b == 0:
        return jsonify({"error": "Division by zero is not allowed."}), 400
    return jsonify({"result": a / b})

if __name__ == "__main__":
    app.run(debug=False)

