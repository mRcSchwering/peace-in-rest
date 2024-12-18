import multiprocessing as mp
import random
import httpx


def _poll(url: str):
    while True:
        print("Polling", url)
        resp = httpx.get(url=url, timeout=1)
        assert resp.status_code == 200, resp.content
        data = resp.json()
        assert len(data) > 0, resp.content


def _create(url: str, payload: dict) -> str:
    print("Creating", url)
    resp = httpx.post(url=url, json=payload, timeout=1)
    assert resp.status_code == 201, resp.content
    data = resp.json()
    return data["pubid"]


def _update(url: str):
    print("Updating", url)
    payload = {"fullname": f"lutz-{random.randint(1, 9999)}"}
    resp = httpx.put(url=url, json=payload, timeout=1)
    assert resp.status_code == 200, resp.content
    data = resp.json()
    assert len(data) > 0, resp.content


def run_deadlocks_test(app_url: str, n_clients: int = 10, **_):
    payload = {"name": "lutz"}
    user_pubid = _create(url=f"{app_url}/users", payload=payload)

    print("Start polling")
    poll_users_kwargs = {"url": f"{app_url}/users/{user_pubid}"}
    poll_users = mp.Process(target=_poll, kwargs=poll_users_kwargs)
    poll_users.start()

    try:
        print("Start updating resources")
        args = [f"{app_url}/users/{user_pubid}" for _ in range(n_clients)]
        with mp.Pool(4) as pool:
            pool.map(_update, args)
        print("Stop updating resources")
    finally:
        print("Stop polling")
        poll_users.kill()
