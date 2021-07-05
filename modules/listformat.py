try:
    from modules.generic.clipboard import Clipboard
except:
    from generic.clipboard import Clipboard


class listformat:
    """Convert an Excel list to a comma separated list for SQL"""

    def __init__(self, config=None):
        self.config = config

    def run(self, param1=None, param2=None):
        current = Clipboard.get_clipboard()

        to_list = current.splitlines()
        formatted = ''

        for row in to_list:
            formatted += f"'{row}',\n"

        formatted = formatted[:-2]
        formatted = f"({formatted})"

        Clipboard.add_to_clipboard(formatted)
        print('list formatted')


if __name__ == '__main__':
    tc = listformat()

    print(tc.__doc__)
