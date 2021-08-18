from modules.generic.clipboard import Clipboard
import xml.dom.minidom


class xmlformat:
    """Format XML from your clipboard"""

    def __init__(self):
        pass

    def __run__(self, params=None):

        c_board = Clipboard.get_clipboard()

        try:
            dom = xml.dom.minidom.parseString(c_board)
            pretty_xml = dom.toprettyxml()
        except:
            print('invalid xml')
            return()

        Clipboard.add_to_clipboard(pretty_xml)
        print('xml formatted')
