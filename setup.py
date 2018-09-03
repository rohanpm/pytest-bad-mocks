import os

from setuptools import setup, find_packages


def get_description():
    return 'A pytest plugin to detect unused mocks'


def get_long_description():
    if os.environ.get('USE_PANDOC') != '1':
        return

    import pypandoc
    converted = pypandoc.convert('README.md', 'rst')

    # The README starts with the same text as "description",
    # which makes sense, but on PyPI causes same text to be
    # displayed twice.  So let's strip that.
    return converted.replace(get_description() + '.\n\n', '', 1)


setup(
    name="pytest-bad-mocks",
    version='1.2.0',
    author='Rohan McGovern',
    author_email='rohan@mcgovern.id.au',
    url='https://github.com/rohanpm/pytest-bad-mocks',
    license='GNU General Public License',
    description=get_description(),
    long_description=get_long_description(),
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["pytest"],
    entry_points={"pytest11": ["bad_mocks = pytest_bad_mocks.plugin"]},
    classifiers=[
        'Framework :: Pytest',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
