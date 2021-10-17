from pegasus.modules.update import update
from pegasus.modules.generic.clipboard import Clipboard
import re


def test_getting_version():
    u = update()

    latest = u.get_latest_version()

    regex_tests = [
        "^v",
        "."
    ]

    for regex in regex_tests:
        assert re.match(regex, latest)


def test_is_latest():
    u = update()

    is_latest = u.is_latest_version()

    assert is_latest in [True, False]


def test_is_most_recent():
    u = update()

    latest = u.get_latest_version()

    current = u.__VERSION__

    assert current == latest


def test_incorrect_command():
    u = update()

    response = u.__run__('incorrect')

    expected = "did you mean to use 'update check' or 'update run'?"

    assert response == expected


def test_subcommands():
    u = update()

    sub = u.subcommands()

    assert sub == ['check', 'run']
