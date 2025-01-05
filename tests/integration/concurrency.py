import multiprocessing as mp
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


def _get(url: str):
    print("Checking", url)
    resp = httpx.get(url=url, timeout=2)
    assert resp.status_code == 200, resp.content
    data = resp.json()
    assert len(data) > 0, data


def _create_user_and_items(user_name: str, app_url: str, n_items=10):
    payload = {"name": user_name, "password": "MyPass1234!"}
    user_pubid = _create(url=f"{app_url}/users", payload=payload)
    for item_i in range(n_items):
        payload = {"name": f"{user_name}_item-{item_i}", "user_pubid": user_pubid}
        item_pubid = _create(url=f"{app_url}/items", payload=payload)
        _get(url=f"{app_url}/items/{item_pubid}")


def run_concurrency_test(
    app_url: str, n_users: int = 10, label: str = "concurrency-test", **_
):
    print("Start polling")
    poll_users_kwargs = {"url": f"{app_url}/users"}
    poll_users = mp.Process(target=_poll, kwargs=poll_users_kwargs)
    poll_users.start()

    try:
        print("Start creating resources")
        args = [(f"{label}_user-{d}", app_url) for d in range(n_users)]
        with mp.Pool(4) as pool:
            pool.starmap(_create_user_and_items, args)
        print("Stop creating resources")
    finally:
        print("Stop polling")
        poll_users.kill()
