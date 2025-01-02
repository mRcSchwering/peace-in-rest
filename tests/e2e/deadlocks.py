import multiprocessing as mp
import random
import httpx


def _poll(url: str):
    while True:
        print("Polling", url)
        resp = httpx.get(url=url, timeout=2)
        assert resp.status_code == 200, resp.content
        data = resp.json()
        assert len(data) > 0, resp.content


def _create(url: str, payload: dict) -> str:
    print("Creating", url)
    resp = httpx.post(url=url, json=payload, timeout=2)
    assert resp.status_code == 201, resp.content
    data = resp.json()
    return data["pubid"]


def _login(url: str, payload: dict) -> str:
    print("Logging in")
    resp = httpx.post(url=url, data=payload, timeout=2)
    assert resp.status_code == 200, resp.content
    data = resp.json()
    return data["access_token"]


def _update(url: str, token: str):
    print("Updating", url)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"fullname": f"lutz-{random.randint(1, 9999)}"}
    resp = httpx.put(url=url, json=payload, headers=headers, timeout=2)
    assert resp.status_code == 200, resp.content
    data = resp.json()
    assert len(data) > 0, resp.content


def run_deadlocks_test(app_url: str, n_clients: int = 10, **_):
    payload = {"name": "lutz", "password": "MyPass123!"}
    user_pubid = _create(url=f"{app_url}/users", payload=payload)

    payload = {"username": "lutz", "password": "MyPass123!"}
    user_token = _login(url=f"{app_url}/auth/token", payload=payload)

    print("Start polling")
    poll_users_kwargs = {"url": f"{app_url}/users/{user_pubid}"}
    poll_users = mp.Process(target=_poll, kwargs=poll_users_kwargs)
    poll_users.start()

    try:
        print("Start updating resources")
        args = [(f"{app_url}/users/{user_pubid}", user_token) for _ in range(n_clients)]
        with mp.Pool(4) as pool:
            pool.starmap(_update, args)
        print("Stop updating resources")
    finally:
        print("Stop polling")
        poll_users.kill()
