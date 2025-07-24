from time import timezone
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from datetime import timedelta, datetime, timezone
from models import User
from sqlmodel import Session
from database import get_sesssion
from schema import Token

SECRET_KEY = "any thing can be secret"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    data_to_encode = data.copy()

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})

    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        new_id: str = str(payload.get("id"))

        if new_id is None:
            raise credentials_exception
        token = Token(id=new_id)
    except JWTError:
        raise credentials_exception
    return token


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_sesssion)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="can't validate user token", headers={"WWW-Authenticate": "Bearer"})
    valid_token = verify_access_token(token, credentials_exception)
    user = session.query(User).filter(User.id == valid_token.id).first()

    return user
