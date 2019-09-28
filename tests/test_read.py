import pytest
import fast_curator.read as fc_read


def test__from_string():
    config = fc_read._from_string("dummy_data_1", {})
    assert len(config) == 1
    assert config["name"] == "dummy_data_1"

    config = fc_read._from_string("dummy_data_2", default=dict(key="val"))
    assert len(config) == 2
    assert config["name"] == "dummy_data_2"
    assert config["key"] == "val"


def test__from_dict():
    dataset = dict(one=1, two="2")

    with pytest.raises(RuntimeError) as e:
        fc_read._from_dict(dataset, {})
    assert "'name'" in str(e)

    dataset["name"] = "test__from_dict"
    config = fc_read._from_dict(dataset, dict(one="one", three=333))

    assert len(config.keys()) == 4
    assert config["one"] == 1
    assert config["two"] == "2"
    assert config["three"] == 333

# def associate_by_ext_suffix(datasets):
# def from_yaml(path, defaults={}, find_associates=associate_by_ext_suffix):
# def get_datasets(datasets_dict, defaults={},
# def _from_string(dataset, default):
# def _from_dict(dataset, default):
