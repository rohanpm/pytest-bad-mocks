from mock import MagicMock
import pytest


@pytest.fixture
def mock_fixture():
    mock = MagicMock()
    yield mock
