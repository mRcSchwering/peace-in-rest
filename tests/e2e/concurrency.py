import os
import multiprocessing as mp
import httpx

APP_URL = os.environ.get("APP_URL", "http://0.0.0.0:8000")


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


def _get(url: str):
    print("Checking", url)
    resp = httpx.get(url=url, timeout=1)
    assert resp.status_code == 200, resp.content
    data = resp.json()
    assert len(data) > 0, data


def _create_user_and_items(user_name: str, n_items=10):
    payload = {"name": user_name}
    user_pubid = _create(url=f"{APP_URL}/users", payload=payload)
    for item_i in range(n_items):
        payload = {"name": f"{user_name}_item-{item_i}", "user_pubid": user_pubid}
        item_pubid = _create(url=f"{APP_URL}/items", payload=payload)
        _get(url=f"{APP_URL}/items/{item_pubid}")


def main(n_users: int = 10):
    print("Start polling")
    poll_users_kwargs = {"url": f"{APP_URL}/users"}
    poll_users = mp.Process(target=_poll, kwargs=poll_users_kwargs)
    poll_users.start()

    try:
        print("Start creating resources")
        user_names = [f"user-{d}" for d in range(n_users)]
        with mp.Pool(4) as pool:
            pool.map(_create_user_and_items, user_names)
        print("Stop creating resources")
    finally:
        print("Stop polling")
        poll_users.kill()


if __name__ == "__main__":
    main()
