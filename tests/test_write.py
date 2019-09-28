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


def test_prepare_contents():
    datasets = [dict(name="foo", one=1, two=2, three="3", a=["ay", "ee", "eye"]),
                dict(name="bar", one="1", two=2, three=3, a=["eye", "oh", "you"]),
                dict(name="baz", one="1", two=2, three="3j", a=["oh"]),
                ]
    contents = fc_write.prepare_contents(datasets)

    assert "defaults" in contents
    assert "datasets" in contents
    assert len(contents["defaults"]) == 2
    assert contents["defaults"]["one"] == "1"
    assert contents["defaults"]["two"] == 2
    assert len(contents["datasets"]) == 3
    assert all("two" not in d for d in contents["datasets"])
    assert "one" not in contents["datasets"][1]
    assert "one" not in contents["datasets"][2]
    assert contents["datasets"][1]["name"] == "bar"
    assert contents["datasets"][2]["name"] == "baz"
    assert all("a" in d for d in contents["datasets"])
