import sqlparse
from modules.generic.clipboard import Clipboard


class sqlformat:
    """Format a SQL query"""

    def __init__(self):
        pass

    def __run__(self, params=None):
        # SELECT * FROM Users
        current = Clipboard.get_clipboard()

        try:
            formatted = sqlparse.format(
                current, reindent=True, keyword_case='upper')
        except:
            print('invalid sql')
            return()

        Clipboard.add_to_clipboard(formatted)
        print('sql formatted')
