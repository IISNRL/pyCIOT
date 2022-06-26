from pyCIOT.data.utils.url import OrderBy


def check_orderby_str(target: str, fields: "list[str]"):
    paths = target.split("=")
    assert len(paths) == 2 and paths[0] == "$orderby"
    extracts = set(paths[1].split(","))
    assert len(extracts) == len(fields) and len(extracts.difference(fields)) == 0


def test_empty_field():
    orderby = OrderBy()
    assert repr(orderby) == ""


def test_init_field():
    orderby = OrderBy(["field1", "field2", "field2", "field3"])
    check_orderby_str(repr(orderby), ["field1 desc", "field2 desc", "field3 desc"])


def test_set_field():
    orderby = OrderBy()
    orderby.set_field("field1").set_field("field2")
    check_orderby_str(repr(orderby), ["field1 desc", "field2 desc"])
    orderby.set_field("field1")
    check_orderby_str(repr(orderby), ["field1 desc", "field2 desc"])


def test_remove_field():
    orderby = OrderBy()
    orderby.set_field("field1").set_field("field2").remove_field("field1")
    check_orderby_str(repr(orderby), ["field2 desc"])
    orderby.remove_field("non_exist")
    check_orderby_str(repr(orderby), ["field2 desc"])
