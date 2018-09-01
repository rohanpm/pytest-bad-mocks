from mock import MagicMock
import pytest


def test_passing():
    assert 1+1 == 2

def test_passing_with_mock_assert(mock_fixture):
    mock_fixture.hello_world()
    mock_fixture.hello_world.assert_called_once()

def test_used_via_mock_calls():
    m = MagicMock()
    assert m.mock_calls == []

def test_used_via_assert():
    m = MagicMock()
    m.assert_not_called()
