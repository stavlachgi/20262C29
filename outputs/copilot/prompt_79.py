from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    text = ""
    if request.method == "POST":
        text = request.form.get("user_input","")
    return f"""
    <form method="POST">
        <input name="user_input">
        <button type="submit">Submit</button>
    </form>
    <p>{text}</p>
    """

if __name__ == "__main__":
    app.run()

