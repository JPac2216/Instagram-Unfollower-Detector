from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = 'bearnroxie'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'followers' not in request.files or 'following' not in request.files:
            flash('Please upload both files.')
            return redirect(request.url)
        followers = request.files['followers']
        following = request.files['following']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if followers.filename == '' or following.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if followers and allowed_file(followers.filename) and following and allowed_file(following.filename):
            filename1 = secure_filename(followers.filename)
            filename2 = secure_filename(following.filename)
            followers.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            following.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            flash('Files uploaded successfully.')
            return redirect(request.url)
        else:
            flash('Please upload JSON files only.')
            return redirect(request.url)
    return render_template('index.html')