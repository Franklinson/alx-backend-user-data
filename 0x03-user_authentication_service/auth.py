#!/usr/bin/env python3
""" Authentication system """

import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """"hashed passwords to bytes"""
    hspwd = password.encode('utf-8')
    return bcrypt.hashpw(hspwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate uuid"""
    id = uuid4()
    return str(id)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a user """
        try:
            usr = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(usr.email))
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate user login """
        try:
            usr = self._db.find_user_by(email=email)
            pwd = password.encode('utf-8')
            return bcrypt.checkpw(pwd, usr.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Generate user sessions """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user using session id"""
        try:
            usr = self._db.find_user_by(session_id=session_id)
            return usr
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy user's session id"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """method to reset password token"""
        try:
            usr = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(usr.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update user password"""
        try:
            usr = self._db.find_user_by(reset_token=reset_token)
            hpw = _hash_password(password)
            self._db.update_user(usr.id, hashed_password=hpw, reset_token=None)
        except NoResultFound:
            raise ValueError
