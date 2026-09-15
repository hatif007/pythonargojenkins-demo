from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Everything is OK - deployed with Argo CD\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)