import os

from flask import redirect, render_template, request, url_for
from werkzeug.utils import redirect, secure_filename

from predictables_flask.app import app

# Ensure the UPLOAD_FOLDER exists and is writable
UPLOAD_FOLDER = "/path/to/the/uploads"
ALLOWED_EXTENSIONS = {"csv", "parquet", "json", "xlsx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def upload_file_form():
    return render_template("upload.html")  # Render a template with the upload form


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return "File uploaded successfully"
    return "Invalid file type"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True)
