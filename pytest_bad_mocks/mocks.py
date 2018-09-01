def check_mocks(mocks):
    for mock in mocks:
        check_mock(mock)


def check_mock(mock):
    calls = mock.mock_calls
    if len(calls) == 0:
        raise UnusedMockError(mock)


class UnusedMockError(AssertionError):
    def __init__(self, unused_mock):
        super(UnusedMockError, self).__init__("Mock was not used: %s" % unused_mock)
