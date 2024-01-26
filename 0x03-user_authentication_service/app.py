#!/usr/bin/env python3
"""python flask app"""


from flask import Flask, jsonify, request, abort, redirect, make_response
from flask import url_for
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
def login() -> str:
    """log in user for the session"""
    email = request.form.get('email', None)
    pswd = request.form.get('password', None)
    details = AUTH.valid_login(email, pswd)
    if not details:
        abort(401)
    session_id = AUTH.create_session(email)
    msg = make_response(jsonify({"email": email, "message": "logged in"}))
    msg.set_cookie("session_id", session_id)
    return msg


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """log out method"""
    sess_id = request.cookies.get('session_id', None)
    if sess_id is None:
        abort(403)
    usr = AUTH.get_user_from_session_id(sess_id)
    if usr is not None:
        AUTH.destroy_session(usr.id)
        return redirect(url_for('root'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ profile for user """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
