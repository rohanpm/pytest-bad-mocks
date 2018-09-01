import logging
import sys
import pytest
import inspect
import os

import _pytest
from _pytest._code import ExceptionInfo

from _pytest.runner import TestReport
from pytest_bad_mocks.mocks import check_mocks
from pytest_bad_mocks.plugin.mock_spy import MockSpy


_LOG = logging.getLogger('pytest-bad-mocks')

logging.basicConfig(level=logging.DEBUG)



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    MockSpy.start()

    yield

    MockSpy.stop()


def pytest_runtest_makereport(item, call):
    if call.when != 'call':
        # report for setup/teardown => don't check
        return

    if call.excinfo:
        # test already raised an exception => don't bother with our check
        return

    bad_mocks = []
    for spy in MockSpy.all():
        if not spy.used:
            bad_mocks.append(spy)

    if not bad_mocks:
        return

    import pdb; pdb.set_trace()
    when = call.when
    duration = call.stop - call.start
    keywords = {x: 1 for x in item.keywords}
    sections = []
    outcome = "failed"
    longrepr = repr_bad_mocks(bad_mocks)
    return TestReport(
        item.nodeid,
        item.location,
        keywords,
        outcome,
        longrepr,
        when,
        sections,
        duration,
        user_properties=item.user_properties,
    )


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

