from flask import Flask, jsonify, render_template, request

# TODO: Add static file paths properly
app = Flask(__name__,
            template_folder="html/index",
            static_url_path="",
            static_folder="html/index")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    # TODO: Add email subscription
    print(f"Email subscribed: {request.form['email']}")
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
