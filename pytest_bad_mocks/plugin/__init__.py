import pytest

import _pytest
from _pytest.outcomes import fail

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
def pytest_runtest_protocol(item, nextitem):
    """Hook wrapping test running to start/stop mock spy."""
    MockSpy.start()
    try:
        yield
    finally:
        MockSpy.stop()


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
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

    fail(repr_bad_mocks(bad_mocks))


def repr_bad_mocks(mock_descriptors):
    if len(mock_descriptors) == 1:
        mock_str = 'Mock'
        was_str = 'was'
    else:
        mock_str = '%s mocks' % len(mock_descriptors)
        was_str = 'were'

    header = '%s created within test %s not used' % (mock_str, was_str)
    out = [header]

    for ds in mock_descriptors:
        out.append('')
        out.append('Mock created at:')
        out.append(format_stack(ds.stack))

    return '\n'.join(out)


def format_stack(stack):
    out = []
    for elem in stack:
        (frame, filename, line, fn, context_lines, context_line) = elem
        if filename.startswith(os.path.dirname(_pytest.__file__)):
            break
        out.append('  %s:%s' % (filename, line))
    return '\n'.join(out)

