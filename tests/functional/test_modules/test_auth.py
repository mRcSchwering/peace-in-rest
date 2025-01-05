import pytest
from jwt.exceptions import InvalidTokenError
from app.modules import auth


def test_hash_and_verify_passwords():
    pw = "MyPassword! [?中"
    pw_hashes = [auth.hash_password(pw=pw) for _ in range(3)]

    assert len(set(pw_hashes)) == 3
    for pw_hash in pw_hashes:
        assert auth.verify_password(pw=pw, pwhash=pw_hash)
        assert not auth.verify_password(pw=pw, pwhash=pw_hash[:-1])


def test_generate_and_decode_tokens():
    secret = "my-secret"
    sub = "a-sub"
    aud = "a-aud"
    add_claims = {"a": [1, "b"]}
    token = auth.generate_token(
        sub=sub, aud=aud, add_claims=add_claims, exp_minutes=1, secret=secret
    )
    claims = auth.decode_token(token=token, aud=aud, secret=secret)

    assert claims["sub"] == sub
    for key in add_claims:
        assert claims[key] == add_claims[key]


@pytest.mark.parametrize(
    "aud, exp_minutes, secret",
    [
        ("a-aud", 1, "another-secret"),
        ("a-aud", -1, "my-secret"),
        ("another-aud", 1, "my-secret"),
    ],
)
def test_invalid_tokens(aud: str, exp_minutes: int, secret: str):
    token = auth.generate_token(
        sub="a-sub", aud="a-aud", exp_minutes=exp_minutes, secret="my-secret"
    )

    with pytest.raises(InvalidTokenError):
        auth.decode_token(token=token, aud=aud, secret=secret)
