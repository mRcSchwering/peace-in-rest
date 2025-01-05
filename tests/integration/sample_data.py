import httpx


def _create(url: str, payload: dict) -> str:
    print("Creating", url)
    resp = httpx.post(url=url, json=payload, timeout=2)
    assert resp.status_code == 201, resp.content
    data = resp.json()
    return data["pubid"]


def add_sample_data(
    app_url: str,
    n_users: int,
    label: str = "sample-data",
    **_,
):
    for user_i in range(n_users):
        username = f"{label}_user-{user_i}"
        payload = {"name": username, "password": f"MyPass123!U{user_i}"}
        user_pubid = _create(url=f"{app_url}/users", payload=payload)
        for item_i in range(user_i):
            payload = {"name": f"{username}_item-{item_i}", "user_pubid": user_pubid}
            _create(url=f"{app_url}/items", payload=payload)
