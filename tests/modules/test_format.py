from pegasus.modules.format import format


def test_json():
    f = format()

    assert 1 == 1

    before = '{"glossary":{"title":"example glossary","GlossDiv":{"title":"S","GlossList":{"GlossEntry":{"ID":"SGML","SortAs":"SGML","GlossTerm":"Standard Generalized Markup Language","Acronym":"SGML","Abbrev":"ISO 8879:1986","GlossDef":{"para":"A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso":["GML","XML"]},"GlossSee":"markup"}}}}}'

    after = f.__run__(['json', before])[1]

    assert before != after


def test_sql():
    f = format()

    before = 'SELECT * FROM users'

    after = f.__run__(['sql', before])[1]

    assert after == 'SELECT *\nFROM users'


def test_xml():
    f = format()

    before = "<note><to>Tove</to><from>Jani</from><heading>Reminder</heading><body>Don't forget me this weekend!</body></note>"

    after = f.__run__(['xml', before])[1]

    assert before != after


def test_list():
    f = format()

    # standard Excel list
    before = """one
                two
                three
                four"""
    expected = "('one', 'two', 'three', 'four')"

    after = f.__run__(['list', before])[1]

    assert after == expected

    # comma separated list
    before = """one, two,three, four"""
    expected = "('one', 'two', 'three', 'four')"

    after = f.__run__(['list', before])[1]

    assert after == expected

    # comma separated list
    before = """one,two,three,four,,,"""
    expected = "('one', 'two', 'three', 'four')"

    after = f.__run__(['list', before])[1]

    assert after == expected
