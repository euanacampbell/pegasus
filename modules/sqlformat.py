import sqlparse
from modules.generic.clipboard import Clipboard

class sqlformat:
    """Format a SQL query"""

    def __init__(self, config=None):
        self.config=config

    def __run__(self, param=None):
        # SELECT * FROM Users
        current = Clipboard.get_clipboard()

        try:
            formatted = sqlparse.format(current, reindent=True, keyword_case='upper')
        except:
            print('invalid sql')
            return()

        Clipboard.add_to_clipboard(formatted)
        print('sql formatted')