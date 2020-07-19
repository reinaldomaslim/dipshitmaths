from flask import Flask, jsonify, render_template, request
import sqlite3
from sqlite3 import Error
from datetime import datetime
from db_handler import *

DATABASE_NAME = r"./sqlite.db"

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
    conn = create_connection(DATABASE_NAME)
    user = [request.form['email'], 0, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"), 0, 0]        
    insert_user(conn, user)
    
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
