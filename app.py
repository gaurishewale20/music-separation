from flask import Flask, request, render_template, send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename
import joblib
import os

# Declare a Flask app
app = Flask(__name__,template_folder='template')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
try:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
except OSError as error:
    print(error)

@app.route('/', methods=['GET', 'POST'])
def main():
    # If a form is submitted
    if request.method == "POST":

        uploadedfile = request.files['audiovar']
        if uploadedfile.filename:
            filename = secure_filename(uploadedfile.filename)
            uploadedfile.save(os.path.join(UPLOAD_FOLDER,filename))
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
	return send_from_directory(UPLOAD_FOLDER,filename, as_attachment=True)

# Running the app
if __name__ == '__main__':
    app.run(debug = True)