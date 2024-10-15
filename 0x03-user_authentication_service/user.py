#!/usr/bin/env python3
"""task0 user.py"""

from sqlalchemy import Column, Integer, String  # Import necessary types
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    """defining user"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """defining string representation"""
        return f"User: id={self.id}"