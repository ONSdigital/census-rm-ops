import pytest
from requests.auth import _basic_auth_str

from app import create_app


@pytest.fixture
def client():
    app = create_app('UnitTestConfig')
    client = app.test_client()
    client.environ_base['HTTP_AUTHORIZATION'] = _basic_auth_str('admin', 'secret')
    yield client