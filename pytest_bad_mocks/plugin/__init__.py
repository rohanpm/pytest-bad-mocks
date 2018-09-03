import pytest

from pytest_bad_mocks.mock_spy import MockSpy

from .report import repr_bad_mocks


# Hooks invoked by pytest.
#
# The reason why we have both pytest_runtest_protocol
# and pytest_pyfunc_call here is so that pytest_runtest_protocol
# sets up the mock spy before any fixtures are created, and
# pytest_pyfunc_call does the mock check inside of the xfail
# hook so that xfails apply to the check.


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):  # noqa pylint: disable=unused-argument
    """Hook wrapping test running to start/stop mock spy."""
    MockSpy.start()
    try:
        yield
    finally:
        MockSpy.stop()


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):  # noqa pylint: disable=unused-argument
    """Hook wrapping test function execution to check mocks
    at the end of a passed test.
    """
    outcome = yield

    if outcome.excinfo:
        # Test already failed for other reasons => no mock check
        return

    bad_mocks = []
    for spy in MockSpy.all():
        if not spy.used:
            bad_mocks.append(spy)

    if not bad_mocks:
        return

    pytest.fail(repr_bad_mocks(bad_mocks))
