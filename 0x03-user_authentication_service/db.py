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


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """ a method to add user
        """
        ad_usr = User(email=email, hashed_password=hashed_password)
        self._session.add(ad_usr)
        self._session.commit()
        return ad_usr

    def find_user_by(self, **kwargs) -> User:
        """ Search method """
        if not kwargs:
            raise InvalidRequestError
        find_usr = self._session.query(User).filter_by(**kwargs).first()
        if not find_usr:
            raise NoResultFound
        return find_usr

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user details"""
        usr = self.find_user_by(id=user_id)
        for key in kwargs.keys():
            if key not in usr.__dict__.keys():
                raise ValueError
            setattr(usr, key, kwargs[key])
        self._session.commit()
