import datetime as dt
import jwt
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from app.config import SECRET_KEY
from app.modules.utils import utcnow


# TODO: how to add refresh?

# TODO: already warnings in passlib...
# WARNING:passlib.handlers.bcrypt:(trapped) error reading bcrypt version
# Traceback (most recent call last):
#   File "/home/marc/anaconda3/envs/pir/lib/python3.11/site-packages/passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
#     version = _bcrypt.__about__.__version__
#               ^^^^^^^^^^^^^^^^^
# AttributeError: module 'bcrypt' has no attribute '__about__'


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(pw: str, pwhash: str) -> bool:
    return bcrypt.checkpw(pw.encode("utf-8"), pwhash.encode("utf-8"))


def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(
    sub: str, aud: str = "app", add_claims: dict | None = None, exp_minutes=30
):
    if add_claims is None:
        add_claims = {}

    exp = utcnow() + dt.timedelta(minutes=exp_minutes)
    claims = {"sub": sub, "aud": aud, "exp": exp}
    return jwt.encode({**add_claims, **claims}, key=SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str | bytes, aud: str = "app") -> dict:
    return jwt.decode(token, audience=aud, key=SECRET_KEY, algorithms=["HS256"])
