import flask
import flask_cors

app = flask.Flask(__name__)
flask_cors.CORS(app, origins=["https://masonacevedo.github.io"])

@app.route('/check-for-bird', methods = ["POST"])
def check_for_bird():
    if flask.request.method == "POST":
        user_input = flask.request.form.get("user_input")
        if user_input is not None:
            return flask.jsonify(contains_bird=("bird" in user_input))
