from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello, LINE Bot!"

if __name__ == "__main__":
    app.run()
