#!/usr/bin/env python3
""" Authentications """

from typing import List, TypeVar
from flask import request
import os


class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Authentication paths """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*":
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is None:
            return None
        header = request.headers.get('Authorization')

        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """ get user """
        return None

    def session_cookie(self, request=None):
        """session cookie"""
        if request is None:
            return None
        if os.environ.get('SESSION_NAME') is not None:
            sess_name = os.environ['SESSION_NAME']
            return request.cookies.get(sess_name)
