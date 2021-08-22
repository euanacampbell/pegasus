from modules.format import format
from modules.generic.clipboard import Clipboard


def test_json():
    f = format()

    before = '{"glossary":{"title":"example glossary","GlossDiv":{"title":"S","GlossList":{"GlossEntry":{"ID":"SGML","SortAs":"SGML","GlossTerm":"Standard Generalized Markup Language","Acronym":"SGML","Abbrev":"ISO 8879:1986","GlossDef":{"para":"A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso":["GML","XML"]},"GlossSee":"markup"}}}}}'
    Clipboard.add_to_clipboard(before)
    f.__run__(['json'])

    after = Clipboard.get_clipboard()

    assert before != after


def test_sql():
    f = format()

    before = 'SELECT * FROM users'
    Clipboard.add_to_clipboard(before)
    f.__run__(['sql'])

    after = Clipboard.get_clipboard()

    assert before != after


def test_xml():
    f = format()

    before = "<note><to>Tove</to><from>Jani</from><heading>Reminder</heading><body>Don't forget me this weekend!</body></note>"
    Clipboard.add_to_clipboard(before)
    f.__run__(['xml'])

    after = Clipboard.get_clipboard()

    assert before != after


def test_list():
    f = format()

    before = """one
                two
                three
                four"""
    Clipboard.add_to_clipboard(before)
    f.__run__(['list'])

    after = Clipboard.get_clipboard()

    assert before != after
