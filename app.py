from flask import Flask
app = Flask(__name__)

SECRET_KEY = '456789vgbnm,ghj567'

@app.route("/")
def home():
    return "Hello Secure CI/CD"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
