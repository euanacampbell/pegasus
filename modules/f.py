import sqlparse
import json
from modules.generic.clipboard import Clipboard


class f:
    'Combined formatter'

    def __init__(self, config=None):
        self.config = config

    def __run__(self, param=None):
        # SELECT * FROM Users
        current = Clipboard.get_clipboard()

        if '\n' in current:
            to_list = current.splitlines()
            formatted = ''

            for row in to_list:
                formatted += f"'{row}',\n"

            formatted = formatted[:-2]
            formatted = f"({formatted})"
            Clipboard.add_to_clipboard(formatted)
            print('list formatted')
            return()

        try:
            parsed = json.loads(current)
            formatted = json.dumps(parsed, indent=4, sort_keys=True)
            Clipboard.add_to_clipboard(formatted)
            print('json formatted')
            return()
        except:
            pass

        try:
            formatted = sqlparse.format(
                current, reindent=True, keyword_case='upper')
            Clipboard.add_to_clipboard(formatted)
            print('sql formatted')
        except:
            print('invalid sql or json')
            return()
