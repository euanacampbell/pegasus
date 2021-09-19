
class test_display:
    'Test different display types'

    def __init__(self):
        pass

    def __run__(self, params=None):

        format_dispatch = {
            'string': 'testing strings',
            'stringinlist': ['testing strings'],
            'int': 42,
            'intinlist': [42],
            'list_of_strings': ['hello', 'my', 'name', 'is', 'test'],
            'list_of_ints': [14, 19, 41, 1242, 0],
            'list_of_lists': [['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test']],
            'list_of_dicts': [{'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}],
            'tablelist': 'test'

        }

        return_all = []

        for format_type in format_dispatch:
            return_all.append(f"%bold%{format_type}")
            return_all.append(format_dispatch[format_type])

        return return_all


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
