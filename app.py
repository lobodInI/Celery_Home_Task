import os
import sqlite3
from flask import Flask, flash, request, redirect, url_for
from celery_worker import task1
from werkzeug.utils import secure_filename
from datetime import datetime



UPLOAD_FOLDER = 'image_folder'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            task_obj = task1.apply_async(args=[file_path])

            con = sqlite3.connect("celery_db")
            cur = con.cursor()
            cur.execute(f"""INSERT INTO info_process (file_name, datetime, status) 
                            VALUES ('{file_path}', '{datetime.now().strftime("%d/%m/%Y  %H:%M:%S")}', 'Add')""")
            con.commit()
            con.close()

            return str(task_obj)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()

