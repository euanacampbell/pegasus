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

        if len(params) == 1:
            c_board = Clipboard.get_clipboard()
        else:
            c_board = " ".join(params[1:])

        return_values = []
        try:
            formatted = format_dispatch[format_type](c_board)
        except:
            raise Exception(f'unable to format to {format_type}')

        try:
            Clipboard.add_to_clipboard(formatted)
        except:
            return_values.append(
                f'Unable to add formatted to clipboard.')

        return_values.append(
            f'Formatted {format_type}.')

        return_values.append(formatted)
        return return_values

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

        if '\n' in to_format:
            to_list = to_format.splitlines()
        elif ',' in to_format:
            to_list = to_format.split(',')
        else:
            to_list = to_format.split(' ')

        to_list = [item.strip() for item in to_list if item.strip() != '']
        formatted = ''

        for row in to_list:
            formatted += f"'{row}', "

        formatted = formatted[:-2]
        formatted = f"({formatted})"

        return formatted
