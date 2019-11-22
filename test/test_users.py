import pytest
from test.utils import reset_testdata, get


user_ids = [1, 2, 3]
reset_testdata()


@pytest.mark.parametrize('user_id', user_ids)
def test_get_user_by_id(user_id):
    resp = get('/users/%d' % user_id)
    assert resp.status_code == 200
    assert resp.json() is not None


def test_get_all_users():
    resp = get('/users/')
    users = resp.json()
    assert isinstance(users, list)
    assert len(users) == 3
