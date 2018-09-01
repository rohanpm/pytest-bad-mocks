from setuptools import setup

setup(
    name="pytest-bad-mocks",
    packages=["pytest_bad_mocks"],
    install_requires=["pytest"],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["bad_mocks = pytest_bad_mocks.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"])
