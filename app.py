from flask import Flask, jsonify, render_template, request, g
from db_handler import DBEngine
from datetime import datetime
from uuid import uuid4

DATABASE_NAME = r"./sqlite.db"
DB_ENGINE = None


def get_db_handler():
    global DB_ENGINE
    if DB_ENGINE is None:
        DB_ENGINE = DBEngine(DATABASE_NAME)
    return DB_ENGINE.handler


app = Flask(__name__,
            template_folder="html/index",
            static_url_path="",
            static_folder="html/index")


@app.route("/", methods=["GET"])
def index():
    print("Index request")
    return render_template("index.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    print("Subscribe request")
    db_handler = get_db_handler()
    referid = str(uuid4())
    try:
        db_handler.insert_email_confirmation(
            email=request.form["email"],
            referid=referid)
    except Exception as e:
        print(e)
        return jsonify(success=False)
    else:
        # TODO: Send verification email
        print(f"Confirmation email added: {request.form['email']}")
        return jsonify(success=True)


@app.route("/confirm", methods=["GET"])
def email_confirmation():
    print("Email confirmation request")
    email = request.values.get("email")
    referid = request.values.get("referid")
    print(f"Email: {email}")
    print(f"Referid: {referid}")
    if email is None or referid is None:
        return jsonify(success=False)

    db_handler = get_db_handler()
    try:
        ret = db_handler.select_email_confirmation(email=email)
        if ret["referid"] == referid:
            db_handler.delete_email_confirmation(email=email)
            db_handler.insert_user(
                email=email,
                purchased=False,
                lastSent=datetime.now(),
                unsubscribed=False,
                deactivated=False)
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    except Exception as e:
        print(e)
        return jsonify(success=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
