import bcrypt


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(plain_password: str):
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
