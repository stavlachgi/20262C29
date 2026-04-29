from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-key'
csrf = CSRFProtect(app)

class SensitiveForm(FlaskForm):
    data = StringField('Data', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SensitiveForm()
    if form.validate_on_submit():
        session['saved_data'] = form.data.data
        return redirect(url_for('success'))
    return render_template_string('''
        <form method="post">
            {{ form.hidden_tag() }}
            {{ form.data.label }} {{ form.data() }}
            {{ form.submit() }}
        </form>
    ''', form=form)

@app.route('/success')
def success():
    return f"Saved: {session.get('saved_data', '')}"

if __name__ == '__main__':
    app.run(debug=True)
