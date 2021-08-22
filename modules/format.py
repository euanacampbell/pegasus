import sqlparse
import json
import xml.dom.minidom

from modules.generic.clipboard import Clipboard


class format:
    'Format various things.'

    def __init__(self):
        pass

    def __run__(self, params=None):

        format_type = params[0]

        format_dispatch = {
            'json': self.format_json,
            'sql': self.format_sql,
            'xml': self.format_xml,
            'list': self.format_list
        }

        if format_type not in format_dispatch:
            print('format not recognised')
            return

        c_board = Clipboard.get_clipboard()
        formatted = format_dispatch[format_type](c_board)
        Clipboard.add_to_clipboard(formatted)

    def format_json(self, to_format):

        try:
            parsed = json.loads(to_format)
        except:
            print('invalid json')
            return to_format

        formatted = json.dumps(parsed, indent=4, sort_keys=True)

        print('json formatted')
        return formatted

    def format_sql(self, to_format):

        try:
            formatted = sqlparse.format(
                to_format, reindent=True, keyword_case='upper')
        except:
            print('invalid sql')
            return

        print('sql formatted')
        return formatted

    def format_xml(self, to_format):

        try:
            dom = xml.dom.minidom.parseString(to_format)
            pretty_xml = dom.toprettyxml()
        except:
            print('invalid xml')
            return

        print('xml formatted')
        return pretty_xml

    def format_list(self, to_format):

        to_list = to_format.splitlines()
        formatted = ''

        for row in to_list:
            formatted += f"'{row}',\n"

        formatted = formatted[:-2]
        formatted = f"({formatted})"

        print('list formatted')
        return formatted
