from flask import Flask, render_template, request
import subprocess
import logging
import socket

app = Flask(__name__)

logging.basicConfig(filename='server.log', level=logging.INFO)

@app.route("/")
def index():
    ip_address = socket.gethostbyname(socket.gethostname())
    return render_template("index.html", ip_address=ip_address)

@app.route("/start_server", methods=["POST"])
def start_server():
    subprocess.Popen(["python", "server.py"])
    logging.info("Server started")
    return "Server started"

@app.route("/log")
def log():
    with open("server.log", "r") as f:
        log_contents = f.read()
    return render_template("log.html", log_contents=log_contents)

if __name__ == '__main__':
    app.run(debug=True)