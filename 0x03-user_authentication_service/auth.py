#!/usr/bin/env python3
""" Authentication system """

import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """"hashed passwords to bytes"""
    hspwd = password.encode('utf-8')
    return bcrypt.hashpw(hspwd, bcrypt.gensalt())
