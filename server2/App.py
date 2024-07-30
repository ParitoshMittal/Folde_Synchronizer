import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from dirsync import sync
from werkzeug.datastructures import FileStorage

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = '1230987'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        source_path = request.form['source_path']
        target_path = request.form['target_path']
        sync(source_path, target_path, 'sync')
        sync(target_path, source_path, 'sync')
        return redirect(url_for('file_viewer', source_path=source_path, target_path=target_path))

    return render_template('index.html')

@app.route('/file_viewer', methods=['GET', 'POST'])
def file_viewer():
    source_path = request.args.get('source_path')
    target_path = request.args.get('target_path')

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
            file.save(os.path.join(source_path, filename))
            sync(source_path, target_path, 'sync')
            sync(target_path, source_path, 'sync')
            return redirect(request.url)

    source_files = os.listdir(source_path)
    target_files = os.listdir(target_path)
    source_folder = os.path.basename(source_path)
    target_folder = os.path.basename(target_path)

    return render_template('file_viewer.html', source_path=source_path, target_path=target_path,
                           source_files=source_files, target_files=target_files,
                           source_folder=source_folder, target_folder=target_folder)

if __name__ == '__main__':
    app.run()
