from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField

app = Flask(__name__)
app.secret_key = "change-this-secret"
csrf = CSRFProtect(app)

class SensitiveForm(FlaskForm):
    submit = SubmitField("Perform sensitive action")

template = """
<!doctype html>
<title>Sensitive Action</title>
<h1>Sensitive Action</h1>
<form method="post">
    {{ form.hidden_tag() }}
    {{ form.submit() }}
</form>
{% if message %}
<p>{{ message }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    form = SensitiveForm()
    message = None
    if form.validate_on_submit():
        session["last_action"] = "Sensitive action performed"
        message = session["last_action"]
    return render_template_string(template, form=form, message=message)

if __name__ == "__main__":
    app.run(debug=True)

