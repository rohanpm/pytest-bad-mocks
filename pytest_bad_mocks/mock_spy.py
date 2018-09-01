import inspect
import os
import sys
from functools import wraps


_CALL_ATTRIBUTES = [
    'called',
    'call_count',
    'call_args',
    'call_args_list',
    'method_calls',
    'mock_calls',
]


def nospy(fn):
    @wraps(fn)
    def out(*args, **kwargs):
        return MockSpy.suspended(fn, *args, **kwargs)
    return out


class MockSpy(object):
    _ALL = []
    _NEW_FN = {}
    _SPY_CLASSES = {}

    def __init__(self, mock):
        self.mock = mock
        self.stack = self._caller_stack()
        self.checked_calls = False
        self.is_child = False

    @classmethod
    def _caller_stack(cls):
        thisdir = os.path.dirname(__file__)
        stack = inspect.stack()
        while stack and stack[0][1].startswith(thisdir):
            stack.pop(0)
        return stack

    @classmethod
    def class_spy_init(cls, mock):
        if not cls._ACTIVE:
            return
        cls._ALL.append(MockSpy(mock))

    @classmethod
    def class_spy_getattribute(cls, mock, name):
        if not cls._ACTIVE:
            return
        spy = cls.spy_for_mock(mock)
        if spy:
            spy.spy_getattribute(name)

    @classmethod
    def class_spy_get_child_mock(cls, _parent, child):
        if not cls._ACTIVE:
            return
        spy = cls.spy_for_mock(child)
        if spy:
            spy.is_child = True

    def spy_getattribute(self, name):
        if name in _CALL_ATTRIBUTES:
            self.checked_calls = True

    @property
    @nospy
    def used(self):
        if self.mock.mock_calls:
            # The mock was used since it was called.
            return True
        if self.checked_calls:
            # The mock was not called, but mock_calls was called
            # (hopefully to verify that the mock was not called...)
            # so it counts as used
            return True
        if self.is_child:
            # The mock was not called, but this mock is the child of
            # another (e.g. created as a MagicMock return value),
            # so it counts as used
            return True

    @classmethod
    def reset(cls):
        cls._ALL = []

    @classmethod
    def all(cls):
        return cls._ALL[:]

    @classmethod
    def start(cls):
        cls._ALL = []
        cls._ACTIVE = True
        mock = sys.modules.get('mock')
        setattr(mock.Mock, '__new__', cls._new_mock)

    @classmethod
    def stop(cls):
        cls._ACTIVE = False
        mock = sys.modules.get('mock')
        delattr(mock.Mock, '__new__')

    @classmethod
    def spy_for_mock(cls, mock):
        for spy in cls._ALL:
            if spy.mock is mock:
                return spy

    @classmethod
    def _new_mock(cls, mock_cls, *_args, **_kwargs):
        mock_cls = cls._mock_subclass(mock_cls)
        return object.__new__(mock_cls)

    @classmethod
    def _mock_subclass(cls, base):
        if base not in cls._SPY_CLASSES:
            cls._SPY_CLASSES[base] = cls._new_mock_subclass(base)
        return cls._SPY_CLASSES[base]

    @classmethod
    def _new_mock_subclass(cls, base):
        def __init__(self, *args, **kwargs):
            base.__init__(self, *args, **kwargs)
            cls.class_spy_init(self)

        def __getattribute__(self, name):
            try:
                return base.__getattribute__(self, name)
            finally:
                cls.class_spy_getattribute(self, name)

        def _get_child_mock(self, *args, **kwargs):
            child = base._get_child_mock(self, *args, **kwargs)  # pylint: disable=protected-access
            cls.class_spy_get_child_mock(self, child)
            return child

        name = base.__name__ + 'Spy'
        klass_dict = {'__init__': __init__,
                      '__getattribute__': __getattribute__,
                      '_get_child_mock': _get_child_mock}
        klass = type(name, (base,), klass_dict)
        return klass

    @classmethod
    def suspended(cls, fn, *args, **kwargs):
        old_active = cls._ACTIVE
        cls._ACTIVE = False
        try:
            return fn(*args, **kwargs)
        finally:
            cls._ACTIVE = old_active
