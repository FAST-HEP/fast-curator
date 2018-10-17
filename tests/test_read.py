import fast_curator.read as fc_read


def test__from_string():
    config = fc_read._from_string("dummy_data_1", {})
    assert len(config) == 1
    assert config["name"] == "dummy_data_1"

    config = fc_read._from_string("dummy_data_2", default=dict(key="val"))
    assert len(config) == 2
    assert config["name"] == "dummy_data_2"
    assert config["key"] == "val"

# def associate_by_ext_suffix(datasets):
# def from_yaml(path, defaults={}, find_associates=associate_by_ext_suffix):
# def get_datasets(datasets_dict, defaults={},
# def _from_string(dataset, default):
# def _from_dict(dataset, default):
