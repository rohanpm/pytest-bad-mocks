from setuptools import setup, find_packages

setup(
    name="pytest-bad-mocks",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["pytest"],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["bad_mocks = pytest_bad_mocks.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"])
