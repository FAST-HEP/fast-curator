import pytest
import fast_curator.read as fc_read


@pytest.fixture
def yaml_config_1(tmpdir):
    content = """
    datasets:
      - name: one
        eventtype: mc
        files: ["{prefix}one", "two"]
        prefix: SOME_prefix/
    """
    tmpfile = tmpdir / "curator_yaml_config_1.yml"
    tmpfile.write(content)
    return str(tmpfile)


@pytest.fixture
def yaml_config_2(yaml_config_1, tmpdir):
    content = """
    import:
      - "{this_dir}/curator_yaml_config_1.yml"
    datasets:
      - name: two
        eventtype: mc
        files: ["one", "two", "{prefix}three"]
        prefix:
          - default: SOME_prefix/
          - second: another_one_PREFIX/
    """
    tmpfile = tmpdir / "curator_yaml_config_2.yml"
    tmpfile.write(content)
    return str(tmpfile)


def test_from_yaml_1(yaml_config_1):
    datasets = fc_read.from_yaml(yaml_config_1)
    assert len(datasets) == 1


def test_from_yaml_2(yaml_config_2):
    datasets = fc_read.from_yaml(yaml_config_2)
    assert len(datasets) == 2


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


def test_apply_prefix():
    files = ["{prefix}one", "{prefix}two/two", "three"]
    dataset = "test_apply_prefix"

    prefix = "testing/"
    result = fc_read.apply_prefix(prefix, files, None, dataset)
    assert len(result) == 3
    assert result[0] == "testing/one"
    assert result[1] == "testing/two/two"
    assert result[2] == "three"

    prefix = [{"default": "another_test/"}, {"second": "yet_another_test/"}]
    result = fc_read.apply_prefix(prefix, files, None, dataset)
    assert len(result) == 3
    assert result[0] == "another_test/one"
    assert result[1] == "another_test/two/two"
    assert result[2] == "three"

    result = fc_read.apply_prefix(prefix, files, "second", dataset)
    assert len(result) == 3
    assert result[0] == "yet_another_test/one"
    assert result[1] == "yet_another_test/two/two"
    assert result[2] == "three"

    with pytest.raises(ValueError) as e:
        fc_read.apply_prefix(prefix, files, "invalid", dataset)
    assert "invalid" in str(e) and "not defined" in str(e)

    prefix = [dict(foo=1, bar=3)]
    with pytest.raises(ValueError) as e:
        fc_read.apply_prefix(prefix, files, None, dataset)
    assert "single-length dict" in str(e)

    prefix = dict(foo=1, bar=3)
    with pytest.raises(ValueError) as e:
        fc_read.apply_prefix(prefix, files, None, dataset)
    assert "string or a list" in str(e)
