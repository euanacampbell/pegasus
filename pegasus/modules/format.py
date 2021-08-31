import sqlparse
import json
import xml.dom.minidom

from pegasus.modules.generic.clipboard import Clipboard


class format:
    'Format json, sql, xml, and sql lists from your clipboard.'

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
            raise Exception('format not recognised')

        c_board = Clipboard.get_clipboard()
        try:
            formatted = format_dispatch[format_type](c_board)
            Clipboard.add_to_clipboard(formatted)
            return f'formatted {format_type}'
        except:
            raise Exception(f'unable to format to {format_type}')

    def format_json(self, to_format):

        parsed = json.loads(to_format)

        formatted = json.dumps(parsed, indent=4, sort_keys=True)

        return formatted

    def format_sql(self, to_format):

        formatted = sqlparse.format(
            to_format, reindent=True, keyword_case='upper')

        return formatted

    def format_xml(self, to_format):

        dom = xml.dom.minidom.parseString(to_format)
        pretty_xml = dom.toprettyxml()

        return pretty_xml

    def format_list(self, to_format):

        to_list = to_format.splitlines()
        formatted = ''

        for row in to_list:
            formatted += f"'{row}',\n"

        formatted = formatted[:-2]
        formatted = f"({formatted})"

        return formatted
