import datetime as dt
import jwt
import bcrypt
from app.modules.utils import utcnow

# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


def hash_password(pw: str) -> str:
    """Hash password and return UTF-8 string of hash"""
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(pw: str, pwhash: str) -> bool:
    """Compare password with password hash and return whether they match"""
    return bcrypt.checkpw(pw.encode("utf-8"), pwhash.encode("utf-8"))


def create_access_token(
    sub: str, aud: str = "app", add_claims: dict | None = None, exp_minutes=60
) -> str:
    """Create JWT with sub, aud, optional additional claims and short exp"""
    if add_claims is None:
        add_claims = {}

    exp = utcnow() + dt.timedelta(minutes=exp_minutes)
    claims = {"sub": sub, "aud": aud, "exp": exp}
    return jwt.encode({**add_claims, **claims}, key=SECRET_KEY, algorithm="HS256")


def create_refresh_token(sub: str, aud: str = "app", exp_minutes=60 * 24) -> str:
    """Create JWT with sub, aud, and long exp"""
    exp = utcnow() + dt.timedelta(minutes=exp_minutes)
    claims = {"sub": sub, "aud": aud, "exp": exp}
    return jwt.encode(claims, key=SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str | bytes, aud: str = "app") -> dict:
    """Verify JWT, decode and return all contained claims"""
    return jwt.decode(token, audience=aud, key=SECRET_KEY, algorithms=["HS256"])
