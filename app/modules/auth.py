import datetime as dt
import jwt
import bcrypt
from app.modules.utils import utcnow


def hash_password(pw: str) -> str:
    """Hash password and return UTF-8 string of hash"""
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(pw: str, pwhash: str) -> bool:
    """Compare password with password hash and return whether they match"""
    return bcrypt.checkpw(pw.encode("utf-8"), pwhash.encode("utf-8"))


def generate_token(
    sub: str,
    secret: str,
    aud: str = "app",
    add_claims: dict | None = None,
    exp_minutes: int = 60,
) -> str:
    """Create JWT with sub, aud, exp and optional additional claims"""
    if add_claims is None:
        add_claims = {}

    exp = utcnow() + dt.timedelta(minutes=exp_minutes)
    claims = {"sub": sub, "aud": aud, "exp": exp}
    return jwt.encode({**add_claims, **claims}, key=secret, algorithm="HS256")


def decode_token(token: str | bytes, secret: str, aud: str = "app") -> dict:
    """Verify JWT, decode and return all contained claims"""
    return jwt.decode(token, audience=aud, key=secret, algorithms=["HS256"])
