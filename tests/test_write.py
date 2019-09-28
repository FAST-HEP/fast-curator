import pytest
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


def test_add_meta():
    dataset = dict(one=1, two="2")
    fc_write.add_meta(dataset, [("three", 3), (4, "four")])

    assert dataset["three"] == 3
    assert dataset[4] == "four"

    with pytest.raises(RuntimeError) as e:
        fc_write.add_meta(dataset, [("one", "3/3")])
    assert "will override" in str(e)
