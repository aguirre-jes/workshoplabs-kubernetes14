from flask import Flask
import os

app = Flask(__name__)

VERSION = os.environ.get("VERSION", "v1")

@app.route("/")
def hello():
    return f"Hello, Kubernetes Folks! Version: {VERSION}"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
