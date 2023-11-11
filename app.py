from flask import Flask, jsonify, render_template, request
from ice_breaker import ice_break

app = Flask(__name__)


@app.route("/process", methods=["POST"])
def process():
    name = request.form.get("name")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    try:
        personIntel, profile_pic_url = ice_break(name)

        # Get the dictionary representation of personIntel
        person_dict = personIntel.to_dict()

        # Add profile_pic_url to the dictionary under the key "picture_url"
        person_dict["picture_url"] = profile_pic_url

        # Return the modified dictionary as JSON
        return jsonify(person_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4000, debug=True)
