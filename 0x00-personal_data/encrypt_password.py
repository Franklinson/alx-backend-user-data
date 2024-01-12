#!/usr/bin/env python3
"""
Password Encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
        Generates a hashed password
        """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed
