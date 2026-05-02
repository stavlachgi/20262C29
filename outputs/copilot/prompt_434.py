from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

form_html = """
<!doctype html>
<title>Upload</title>
<h1>Upload file</h1>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="Upload">
</form>
<p>{{ message }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def upload():
    message = ""
    if request.method == "POST":
        f = request.files.get("file")
        if f and f.filename:
            path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
            f.save(path)
            message = f"Uploaded to {path}"
        else:
            message = "No file selected"
    return render_template_string(form_html, message=message)

if __name__ == "__main__":
    app.run(debug=True)

