from flask import Flask, render_template_string, request

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Input</title>
</head>
<body>
    <form method="POST">
        <input type="text" name="user_text" placeholder="Enter something...">
        <button type="submit">Submit</button>
    </form>
    {% if output %}
        <h1>You entered: {{ output }}</h1>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        output = request.form.get("user_text")
    return render_template_string(template, output=output)

if __name__ == "__main__":
    app.run(debug=True)
