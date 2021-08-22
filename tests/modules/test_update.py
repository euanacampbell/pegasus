from modules.update import update
from modules.generic.clipboard import Clipboard
import re


def test_getting_version():
    u = update()

    latest = u.get_latest_version()

    test_examples = []

    test_examples.append(re.match("^v", latest))
    test_examples.append(re.match(".", latest))
    test_examples.append(re.match("^v(\d+\.)?(\d+\.)?(\*|\d+)$", latest))

    for test_result in test_examples:
        assert test_result
