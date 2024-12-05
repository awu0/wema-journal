import data.manuscripts.fields as mflds


def test_get_fields():
    assert isinstance(mflds.get_fields(), dict)


def test_get_field_names():
    fld_names = mflds.get_field_names()
    assert isinstance(fld_names, dict_keys)
    assert all(isinstance(name, str) for name in fld_names) 