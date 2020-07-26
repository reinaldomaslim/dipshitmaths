from flask import Flask, jsonify, render_template, request, g
from db_handler import DBHandler
from datetime import datetime

DATABASE_NAME = r"./sqlite.db"


def get_db_handler():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DBHandler(DATABASE_NAME)
    return db


app = Flask(__name__,
            template_folder="html/index",
            static_url_path="",
            static_folder="html/index")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    try:
        engine = get_db_handler()
        engine.insert_user(
            email=request.form["email"],
            purchased=False,
            lastSent=datetime.now(),
            unsubscribed=False,
            deactivated=False
        )
        print(f"Email subscribed: {request.form['email']}")
        return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
