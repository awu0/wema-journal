import data.manuscripts.fields as mflds


def test_get_flds():
    assert isinstance(mflds.get_flds(), dict)


def test_get_fld_names():
    fld_names = mflds.get_fld_names()
    assert isinstance(fld_names, list)
    assert all(isinstance(name, str) for name in fld_names) 