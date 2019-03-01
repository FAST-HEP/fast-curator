import fast_curator.write as fc_write


def test_select_default():
    default = fc_write.select_default([0, 1, 2, 2, 2, 3])
    assert default == 2

    default = fc_write.select_default([0, 1, 2, 3])
    assert default is None

    default = fc_write.select_default([0, 1, 2, 2, 3, 3])
    assert default is None

    default = fc_write.select_default([])
    assert default is None
