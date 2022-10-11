from flask import send_file
from flask import Flask
# from read import try_this
from flask import jsonify
from flask import json
app = Flask(__name__)


@app.route('/scores')
def send_scores_file():

    return send_file("live_scores.txt")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
