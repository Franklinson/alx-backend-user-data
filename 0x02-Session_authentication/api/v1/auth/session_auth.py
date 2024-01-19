#!/usr/bin/env python3
"""a session_auth class"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session auth class """
