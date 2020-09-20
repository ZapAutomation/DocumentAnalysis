#!/usr/bin/env python
import uuid
import os
import shutil
import urllib.request
import subprocess
import time
# from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, flash, request, redirect, send_file
from flask_talisman import Talisman
from threading import Thread
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['pdf', 'txt'])

curr_dir = os.getcwd()

UPLOAD_FOLDER = curr_dir

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
Talisman(app, content_security_policy=None)
# run_with_ngrok(app)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024


def create_queue():
    queue = []
    return queue

queue = create_queue()

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')

        queue.append(str(request.remote_addr)) 
        while queue[0] != str(request.remote_addr):
            time.sleep(15)

        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], str(request.remote_addr).replace(".", ""))):
            shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'], str(request.remote_addr).replace(".", "")))   
        
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], str(request.remote_addr).replace(".", "")))
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(request.remote_addr).replace(".", ""), filename))
        flash('File(s) successfully uploaded')

        subprocess.call([os.path.join(curr_dir, 'clean.sh')])

        for dirpath, dirname, files in os.walk(os.path.join(app.config['UPLOAD_FOLDER'], str(request.remote_addr).replace(".", ""))):
            for file in files:
                shutil.move(os.path.join(app.config['UPLOAD_FOLDER'], str(request.remote_addr).replace(".", ""), file), app.config['UPLOAD_FOLDER'])

        for dirpath, dirname, files in os.walk('.'):
            for file in files:
                if file[-4:] == '.pdf':
                    shutil.move(os.path.join(dirpath, file), os.path.join(curr_dir, documents, pdfs, file))

        subprocess.call([os.path.join(curr_dir, 'execute.sh')])
        time.sleep(2)
        del queue[0]
        return redirect('/results')

@app.route("/results")
def results():
    try:
        return send_file(os.path.join(curr_dir,'results.zip'), as_attachment=True, attachment_filename='results_' +str(uuid.uuid4()) + '.zip', cache_timeout=0)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
	app.run('0.0.0.0', port=80)

