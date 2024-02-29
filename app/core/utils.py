from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any
from ..settings import conf
import logging
import sys

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWT:
    @staticmethod
    def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=conf.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, conf.JWT_SECRET_KEY, algorithm=conf.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: str, expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=conf.REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, conf.JWT_REFRESH_SECRET_KEY, conf.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)



