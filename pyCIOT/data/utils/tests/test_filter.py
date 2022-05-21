from pyCIOT.data.utils.url import Filter
from pyCIOT.data.utils import op

def test_empty_field():
    filter = Filter()
    assert repr(filter) == ""

def test_init_field():
    filter = Filter(filters=[op.EQ("field1", "value1"), op.GT("field2", "value2"), op.GT("field2", "value2")])
    assert repr(filter) == "$filter=field1 eq 'value1' and field2 gt 'value2'"

def test_set_field():
    filter = Filter()
    filter.set_filter(op.EQ("field1", "value1")).set_filter(op.EQ("field1", "value1")).set_filter(op.GT("field2", "value2"))
    assert repr(filter) == "$filter=field1 eq 'value1' and field2 gt 'value2'"

def test_remove_field():
    filter = Filter()
    filter.set_filter(op.EQ("field1", "value1")).set_filter(op.EQ("field2", "value2"))
    filter.remove_filter(op.EQ("field2", "value2"))
    assert repr(filter) == "$filter=field1 eq 'value1'"
