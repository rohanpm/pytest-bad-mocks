from mock import MagicMock
import pytest

pytestmark = [pytest.mark.xfail(strict=True)]


def test_failing():
    raise ValueError('oops!')


def test_failing_via_mock(mock_fixture):
    mock_fixture.hello_world.assert_called_once()


def test_useless_mock():
    m = MagicMock()
    assert 1+1 == 2


def test_useless_mock_from_fixture(mock_fixture):
    assert 1+1 == 2

