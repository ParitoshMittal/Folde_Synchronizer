from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        server_ip = request.form['server_ip']
        cmd = ['python', 'client_script.py', server_ip]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if stderr:
            return f'Error syncing files: {stderr}'
        else:
            return f'Files synced successfully: {stdout}'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
