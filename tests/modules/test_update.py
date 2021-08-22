from modules.update import update
from modules.generic.clipboard import Clipboard
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
