from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
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

            result = comparsion()

            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            return render_template('index.html', result = result)
        else:
            flash('Please upload JSON files only.')
            return redirect(request.url)
    return render_template('index.html')
        
        
def comparsion():
    followers = set()
    following = set()
    with open(os.path.join(UPLOAD_FOLDER, 'followers_1.json'), 'r') as file1:
        followers_json = json.load(file1)
        for user in followers_json:
            if 'string_list_data' in user:
                data = user['string_list_data']
                followers.add((data[0]['value']))

    with open(os.path.join(UPLOAD_FOLDER, 'following.json'), 'r') as file2:
        following_json = json.load(file2)
        for user in following_json["relationships_following"]:
            if 'string_list_data' in user:
                data = user['string_list_data']
                following.add((data[0]['value']))

    not_followed_back = following - followers  

    return not_followed_back