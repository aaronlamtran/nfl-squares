from flask import Flask
from read import try_this
from flask import jsonify
from flask import json
app = Flask(__name__)


@app.route('/try_this')
def return_something():

    data = try_this()

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
