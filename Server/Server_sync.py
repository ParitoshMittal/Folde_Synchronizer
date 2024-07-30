import socket
import os
import time
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

try:
    os.mkdir("server_folder")
except FileExistsError:
    pass

@app.route('/')
def home():
    ip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', ip=ip)

@app.route("/")
def redirect_to_path():
    path = 'C:/Users/Lenovo/Desktop/Os/server_folder'
    return redirect(url_for('path'))

@app.route('/sync/files', methods=['POST'])
def send_file():
    ip = socket.gethostbyname(socket.gethostname())
    port = 1234
    path = './server_folder'
    file_dict = {}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen(5)

        while True:
            update = []
            new_dict = {}
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    modified_time = os.path.getmtime(file_path)
                    new_dict[file_path] = modified_time

            for file_path, modified_time in new_dict.items():
                if file_path not in file_dict:
                    update.append(os.path.basename(file_path))
                elif modified_time > file_dict[file_path]:
                    update.append(os.path.basename(file_path))

            file_dict = new_dict

            for filename in update:
                conn, addr = s.accept()

                file_info = f"{os.path.getsize(os.path.join(path, filename))}|{filename}".encode('utf-8')
                conn.sendall(file_info)

                with open(os.path.join(path, filename), "rb") as f:
                    file_data = f.read()

                conn.sendall(file_data)

                print(f"\n{filename} file synced\n")

                conn.close()

            time.sleep(1)

if __name__ == '__main__':
    app.run(debug=True)
