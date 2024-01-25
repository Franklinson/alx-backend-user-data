#!/usr/bin/env python3
"""python flask app"""


from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root():
    """homepage of this application"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """register user using the application"""
    email = request.form.get('email', None)
    pwd = request.form.get('password', None)
    try:
        usr = AUTH.register_user(email, pwd)
        return jsonify({"email": usr.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """log in user"""
    email = request.form.get('email', None)
    pswd = request.form.get('password', None)
    details = AUTH.valid_login(email, pswd)
    if not details:
        abort(401)
    s_id = AUTH.create_session(email)
    msg = make_response(jsonify({"email": email, "message": "logged in"}))
    msg.set_cookie("session_id", s_id)
    return msg


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
