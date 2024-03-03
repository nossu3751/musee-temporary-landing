import re
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    origins = ["*"]
    CORS(app, origins=origins, supports_credentials=True)

    @app.route("/", methods=["GET"])
    def home():
        return "ok", 200

    @app.route("/mailList", methods=["POST"])
    def addMail():
        def _is_email(email):
            regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
           
            if re.match(regex, email, re.IGNORECASE):
                return True
            else:
                return False
        def _exists(email):
            if os.path.exists("emails.txt"):
                with open("emails.txt") as f:
                    for line in f.readlines():
                        if email in line:
                            return True
            return False
            
        data = request.json
        if not data or "email" not in data:
            return jsonify("not posted"), 409
        else:
            email = data["email"]
            if _is_email(email) and not _exists(email):
                with open("emails.txt", 'a') as f:
                    f.write(email+"\n")
                return jsonify("ok"), 201
            return jsonify("not posted"), 409
    return app

app = create_app()