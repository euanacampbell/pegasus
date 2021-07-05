import json
from modules.generic.clipboard import Clipboard


class jsonformat:
    """Format a JSON object"""

    def __init__(self, config=None):
        self.config = config

    def __run__(self, param1=None, param2=None):
        current = Clipboard.get_clipboard()

        try:
            parsed = json.loads(current)
        except:
            print('invalid json')
            return()
        formatted = json.dumps(parsed, indent=4, sort_keys=True)

        Clipboard.add_to_clipboard(formatted)
        print('json formatted')
