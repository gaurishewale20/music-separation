from flask import Flask, request, render_template, send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename
import joblib
import os

# Declare a Flask app
app = Flask(__name__,template_folder='template')

app.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(app.config['APP_ROOT'], 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.mp3', '.wav']

try:
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
except OSError as error:
    print(error)

@app.errorhandler(413)
def too_large(e):
    return "</h1> File is too large </h1> <h3><a href='/'> Try again </a></h3>", 413

@app.route('/', methods=['GET', 'POST'])
def main():
    # If a form is submitted
    if request.method == "POST":

        uploadedfile = request.files['audiovar']
        if uploadedfile.filename:
            filename = secure_filename(uploadedfile.filename)
            file_ext = os.path.splitext(filename)[1]
            print(file_ext)
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return "<h1> Invalid file type. <h1> <h3><a href='/'> Try again </a></h3>", 400
            uploadedfile.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(uploadedfile.filename)
         # Unpickle Model
        # clf = joblib.load("clf.pkl")

        # Put input into suitable format

        # Get prediction
        # prediction = clf.predict(X)
            return render_template('website.html', filename=filename, vocalsfilename= filename, drumsfilename=filename, bassfilename=filename, otherfilename=filename)
    else:
        filename = ""

    return render_template("website.html", filename=filename)

@app.route('/uploads/<filename>')
def uploaded_song(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)

# Running the app
if __name__ == '__main__':
    app.run(debug = True)