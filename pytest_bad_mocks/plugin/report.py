import os
import _pytest


def repr_bad_mocks(mock_spies):
    if len(mock_spies) == 1:
        mock_str = 'Mock'
        was_str = 'was'
    else:
        mock_str = '%s mocks' % len(mock_spies)
        was_str = 'were'

    header = '%s created within test %s not used' % (mock_str, was_str)
    out = [header]

    for ds in mock_spies:
        out.append('')
        out.append('Mock created at:')
        out.append(format_stack(ds.stack))

    return '\n'.join(out)


def format_stack(stack):
    out = []
    for elem in stack:
        (_, filename, line, _, _, _) = elem
        if filename.startswith(os.path.dirname(_pytest.__file__)):
            break
        out.append('  %s:%s' % (filename, line))
    return '\n'.join(out)

