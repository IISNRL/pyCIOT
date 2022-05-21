from pyCIOT.data.utils.url import Select

def check_select_str(target: str, fields: list[str]):
    paths = target.split("=")
    assert len(paths) == 2 and paths[0] == "$select"
    extracts = set(paths[1].split(","))
    assert len(extracts) == len(fields) and len(extracts.difference(fields)) == 0

def test_empty_field():
    select = Select()
    assert repr(select) == ""

def test_init_field():
    select = Select(["field1", "field2", "field2", "field3"])
    check_select_str(repr(select), ["field1", "field2", "field3"])

def test_set_field():
    select = Select()
    select.set_field("field1").set_field("field2")
    check_select_str(repr(select), ["field1", "field2"])
    select.set_field("field1")
    check_select_str(repr(select), ["field1", "field2"])

def test_remove_field():
    select = Select()
    select.set_field("field1").set_field("field2").remove_field("field1")
    check_select_str(repr(select), ["field2"])
    select.remove_field("non_exist")
    check_select_str(repr(select), ["field2"])
