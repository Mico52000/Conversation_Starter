from flask import Flask, jsonify, render_template, request
from ice_breaker import ice_break

app = Flask(__name__)


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    personIntel, profile_pic_url = ice_break(name)
    return jsonify(personIntel.to_dict())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
