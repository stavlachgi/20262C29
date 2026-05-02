from flask import Flask, request, redirect, url_for, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

html = '''
<!doctype html>
<title>Upload File</title>
<h1>Upload File</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(path)
            return redirect(url_for('upload_file'))
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
