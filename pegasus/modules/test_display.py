import sqlparse
import json
import xml.dom.minidom

from pegasus.modules.generic.clipboard import Clipboard


class test_display:
    'Test different display types'

    def __init__(self):
        pass

    def __run__(self, params=None):

        format_type = params[0]

        format_dispatch = {
            'string': 'testing strings',
            'stringinlist': ['testing strings'],
            'int': 42,
            'intinlist': [42],
            'los': ['hello', 'my', 'name', 'is', 'test'],
            'loi': [14, 19, 41, 1242, 0],
            'lol': [['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test']],
            'lod': [{'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}],
            'tablelist': 'test'

        }

        return format_dispatch[format_type]


"""
string
int
list of string los 
list of int loi
list of list lol
list of dict lod
dict of string dos
dict of int doi
dict of list dol
dict of dict  dod
table
"""
