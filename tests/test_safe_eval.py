import pytest
from mkdocs_table_reader_plugin.safe_eval import safe_eval, parse_argkwarg


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
    myString = "'\s+'"
    assert safe_eval(myString) == "\s+"


def test_safe_eval4():
    myString = "','"
    assert safe_eval(myString) == ","


def test_safe_eval5():
    myString = "None"
    assert safe_eval(myString) == None


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
