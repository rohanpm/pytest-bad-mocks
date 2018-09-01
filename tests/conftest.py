from mock import MagicMock, Mock
import pytest


@pytest.fixture
def mock_fixture():
    mock = MagicMock()
    yield mock

