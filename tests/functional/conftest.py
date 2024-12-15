import pytest
from httpx import AsyncClient, ASGITransport
from pytest_asyncio import is_async_test
from app.main import app


def pytest_collection_modifyitems(items):
    # NOTE: makes sure that all async tests run in the same event loop
    #       it is recommended to do it like this (see pytest-asyncio howto guides)
    #       not doing this leads to "RunTimeError: Task got Future attached to different loop"
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="function")
async def api_client():
    asgi_transport = ASGITransport(app=app)
    async with AsyncClient(transport=asgi_transport, base_url="http://test") as client:
        yield client
