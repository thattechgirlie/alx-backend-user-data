#!/usr/bin/env python3
""" Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """ password hash"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ validity function """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
