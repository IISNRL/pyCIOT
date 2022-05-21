from pyCIOT.data.utils.url import Pagination

def test_empty():
    pagination = Pagination()
    assert repr(pagination) == "$top=1"

def test_init_start():
    pagination = Pagination(start=3)
    assert repr(pagination) == "$skip=2&$top=1"

def test_init_end():
    pagination = Pagination(end=6)
    assert repr(pagination) == "$top=5"

def test_init_start_end():
    pagination = Pagination(start=10, end=20)
    assert repr(pagination) == "$skip=9&$top=10"

def test_init_invalid():
    try:
        Pagination(start=-1, end=20)
        assert False
    except:
        assert True

    try:
        Pagination(start=10, end=10)
        assert False
    except:
        assert True

    try:
        Pagination(start=0, end=-100)
        assert False
    except:
        assert True

def test_set_delimiter():
    pagination = Pagination(start=10)
    pagination.set_delimiter("|")
    assert repr(pagination) == "$skip=9|$top=1"
    pagination.set_delimiter("-")
    assert repr(pagination) == "$skip=9-$top=1"

def test_set_start():
    pagination = Pagination(1, 11)
    pagination.set_start(10)
    assert repr(pagination) == "$skip=9&$top=1"

def test_set_end():
    pagination = Pagination()
    pagination.set_end(10)
    assert repr(pagination) == "$top=9"

def test_set_invalid_start():
    pagination = Pagination(end=10)
    try:
        pagination.set_start(10)
        assert False
    except:
        assert True

    try:
        pagination.set_start(-1)
        assert False
    except:
        assert True

def test_set_invalid_end():
    pagination = Pagination(start=30)
    try:
        pagination.set_end(10)
        assert False
    except:
        assert True

    try:
        pagination.set_start(-1)
        assert False
    except:
        assert True
