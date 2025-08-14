from flask import Flask
import os
import socket

app = Flask(__name__)

VERSION = os.environ.get("VERSION", "v1")

@app.route("/")
def hello():
    hostname = socket.gethostname()
    if VERSION == "1.0.0":
        msg = "Hello, Kubernetes Folks, this is the initial version!"
    elif VERSION == "1.1.0":
        msg = "Hello, Kubernetes Folks, this is the intermediate version!"
    elif VERSION == "1.2.0":
        msg = "Hello, Kubernetes Folks, this is the final version!"
    else:
        msg = "Hello, Kubernetes Folks, unknown version!"
    return f"{msg} Version: {VERSION} | Host: {hostname}"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
