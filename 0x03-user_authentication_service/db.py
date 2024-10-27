#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import TypeVar

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """DB class to handle database operations
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None


    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the Database and returns the User object.
        """
        if not email or not hashed_password:
            raise ValueError("Email and hashed_password must be provided")

        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        try:
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            print(f"An error occurred while adding the user: {e}")
            raise

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a User in the Database based on keyword arguments.
        Raises NoResultFound if the user is not found.
        """
        if not kwargs:
            raise InvalidRequestError("No search parameters provided")

        if any(key not in VALID_FIELDS for key in kwargs):
            raise InvalidRequestError("Invalid search parameters")

        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("User not found with the specified parameters")
        except Exception as e:
            print(f"An error occurred during find_user_by: {e}")
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.
        Only fields listed in VALID_FIELDS can be updated.
        """
        if not kwargs:
            raise ValueError("No attributes provided to update")

        session = self._session
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if key not in VALID_FIELDS:
                    raise ValueError(f"{key} is not a valid field")
                setattr(user, key, value)
            session.commit()
        except NoResultFound:
            print(f"No user found with id {user_id}")
            raise
        except Exception as e:
            session.rollback()
            print(f"An error occurred while updating the user: {e}")
            raise
