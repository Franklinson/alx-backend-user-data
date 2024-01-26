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


@app.route('/profile', strict_slashes=False)
def profile():
    """ User profile """
    sess_id = request.cookies.get('session_id', None)
    if sess_id is None:
        abort(403)
    usr = AUTH.get_user_from_session_id(sess_id)
    if usr is not None:
        return jsonify({"email": usr.email})
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Reset user password"""
    try:
        email = request.form.get('email', None)
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """update user password"""
    email = request.form.get('email', None)
    reset_token = request.form.get('reset_token', None)
    new_password = request.form.get('new_password', None)
    if email is None or reset_token is None or new_password is None:
        abort(403)
    try:
        actual_token = AUTH.get_reset_password_token(email)
        if actual_token != reset_token:
            abort(403)
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
