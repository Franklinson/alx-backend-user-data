#!/usr/bin/env python3
""" Basic auth authentication """

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic auth """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Implementing Basic64 """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token
