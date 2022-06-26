import datetime
from pyCIOT.data.utils.op import OP, EQ, LE, LT, GE, GT, SUBSTRING

comparisons: "list[OP]" = [EQ, LE, LT, GE, GT]


def test_eq():
    op = EQ("field", "value")
    assert op.get_expression() == "field eq 'value'"


def test_le():
    op = LE("field", "value")
    assert op.get_expression() == "field le 'value'"


def test_lt():
    op = LT("field", "value")
    assert op.get_expression() == "field lt 'value'"


def test_GE():
    op = GE("field", "value")
    assert op.get_expression() == "field ge 'value'"


def test_GT():
    op = GT("field", "value")
    assert op.get_expression() == "field gt 'value'"


def test_substring():
    substring = SUBSTRING("field", "value")
    assert substring.get_expression() == "substringof('value',field)"


def test_transformation():
    test_date = "2022-01-01T01:23:45Z"

    # Datetime (isoformat only accept 2022-01-01T01:23:45)
    date = datetime.datetime.fromisoformat(test_date[:-1])
    assert OP.transform(date) == test_date

    # Date string
    assert OP.transform(test_date) == test_date

    # Values
    assert OP.transform(1) == 1
    assert OP.transform(1.33) == 1.33
    assert OP.transform("test") == "'test'"
