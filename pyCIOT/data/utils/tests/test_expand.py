from pyCIOT.data.utils.url import Expand, Expands
from pyCIOT.data.utils.url import Select, Filter
from pyCIOT.data.utils.op import EQ, GT

def test_empty():
    expand = Expand(name="field")
    assert repr(expand) == "field"

def test_add_query():
    expand = Expand(name="field", select=Select(["field1"]), filter=Filter([EQ("f", "v")]))
    assert repr(expand) == "field($select=field1;$filter=f eq 'v')"

def test_expands():
    expand1 = Expand(name="field1", select=Select(["field1"]))
    expand2 = Expand(name="field2", filter=Filter([EQ("f", "v")]))

    expands = Expands([expand1, expand2])
    assert repr(expands) == "$expand=field1($select=field1),field2($filter=f eq 'v')"



