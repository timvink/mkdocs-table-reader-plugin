import pytest

from mkdocs_table_reader_plugin.safe_eval import parse_argkwarg, safe_eval


def test_safe_eval0():
    myString = "'\r'"
    assert safe_eval(myString) == "\r"


def test_safe_eval1():
    myString = "'\r\t'"
    assert safe_eval(myString) == "\r\t"


def test_safe_eval2():
    myString = "'\n'"
    assert safe_eval(myString) == "\n"


def test_safe_eval3():
    myString = r"'\s+'"
    assert safe_eval(myString) == r"\s+"


def test_safe_eval4():
    myString = "','"
    assert safe_eval(myString) == ","


def test_safe_eval5():
    myString = "None"
    assert safe_eval(myString) is None


def test_parseargkwarg_1():
    s = "title='bah', name='john', purple='haze', none=None, i=1"
    args, kwargs = parse_argkwarg(s)
    assert args == []
    assert kwargs == {
        "title": "bah",
        "name": "john",
        "purple": "haze",
        "none": None,
        "i": 1,
    }


def test_parseargkwarg_2():
    s = "'assets/tables/table.csv'"
    args, kwargs = parse_argkwarg(s)
    assert args == ["assets/tables/table.csv"]
    assert kwargs == {}


def test_parseargkwarg_3():
    s = "'assets/tables/table.csv', sep=','"
    args, kwargs = parse_argkwarg(s)
    assert args == ["assets/tables/table.csv"]
    assert kwargs == {"sep": ","}


def test_parseargkwarg_4():
    s = "'assets/tables/table.csv', sep='\r\t'"
    args, kwargs = parse_argkwarg(s)
    assert args == ["assets/tables/table.csv"]
    assert kwargs == {"sep": "\r\t"}


def test_parseargkwarg_5():
    s = "'assets/tables/table.csv', sep = '\r\t'"
    args, kwargs = parse_argkwarg(s)
    assert args == ["assets/tables/table.csv"]
    assert kwargs == {"sep": "\r\t"}


def test_parseargkwarg_6():
    s = "'assets/tables/table.csv' ,  sep = '\r\t'"
    args, kwargs = parse_argkwarg(s)
    assert args == ["assets/tables/table.csv"]
    assert kwargs == {"sep": "\r\t"}


def test_parseargkwarg_7():
    s = "'table with space.csv', sep = '\r\t'"
    args, kwargs = parse_argkwarg(s)
    assert args == ["table with space.csv"]
    assert kwargs == {"sep": "\r\t"}


def test_parseargkwarg_error():

    with pytest.raises(AssertionError):
        s = "'assets/tables/table.csv', sep = '\r\t', 'another path'"
        args, kwargs = parse_argkwarg(s)


def test_parseargkwarg_equals_sign_in_value():
    """
    An '=' inside a value is not the separator between a key and a value.
    """
    args, kwargs = parse_argkwarg("'a=b.csv'")
    assert args == ["a=b.csv"]
    assert kwargs == {}

    args, kwargs = parse_argkwarg("'table.csv', sep='='")
    assert args == ["table.csv"]
    assert kwargs == {"sep": "="}

    args, kwargs = parse_argkwarg("'table.csv', na_values=['a=1']")
    assert args == ["table.csv"]
    assert kwargs == {"na_values": ["a=1"]}


def test_parseargkwarg_nested_values():
    """
    A comma inside a list, tuple or dict does not separate two arguments.
    """
    args, kwargs = parse_argkwarg("'table.csv', usecols=[0, 1]")
    assert args == ["table.csv"]
    assert kwargs == {"usecols": [0, 1]}

    args, kwargs = parse_argkwarg("'table.csv', names=('a', 'b')")
    assert args == ["table.csv"]
    assert kwargs == {"names": ("a", "b")}

    args, kwargs = parse_argkwarg("'table.csv', dtype={'a': 'str', 'b': 'int'}")
    assert args == ["table.csv"]
    assert kwargs == {"dtype": {"a": "str", "b": "int"}}
