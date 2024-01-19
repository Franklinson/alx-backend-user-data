#!/usr/bin/env python3
"""a session_auth class"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Session function"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)
