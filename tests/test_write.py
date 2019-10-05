import os
import pytest
import fast_curator.write as fc_write
import fast_curator.catalogues as catalogues


@pytest.fixture
def dummy_file_dir():
    directory = os.path.dirname(__file__)
    directory = os.path.join(directory, "dummy_files")
    assert os.path.isdir(directory)
    return directory


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
    datasets = [dict(name="foo", one="i1", two=2, three="3", a=["ay", "ee", "eye"]),
                dict(name="bar", one="1", two=2, three="3i", a=["eye", "oh", "you"]),
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


@pytest.mark.parametrize("expand", ["xrootd", "local"])
@pytest.mark.parametrize("nfiles,nevents,empty",
                         [(2, 302, True), (4, 302, False)])
def test_prepare_file_list(dummy_file_dir, nfiles, nevents, empty, expand):
    tree = "events"
    files = os.path.join(dummy_file_dir, "*.root")
    file_list = fc_write.prepare_file_list(files, "data", "mc", tree_name=tree,
                                           expand_files=expand,
                                           confirm_tree=False,
                                           no_empty_files=empty)

    assert isinstance(file_list, dict)
    assert file_list["name"] == "data"
    assert file_list["eventtype"] == "mc"
    assert file_list["nfiles"] == nfiles
    assert file_list["nevents"] == nevents


@pytest.mark.parametrize("expand", ["xrootd", "local"])
@pytest.mark.parametrize("empty", [True, False])
def test_prepare_file_list_confirm_trees(dummy_file_dir, empty, expand):
    tree = "events"
    files = os.path.join(dummy_file_dir, "*.root")
    with pytest.raises(RuntimeError) as e:
        fc_write.prepare_file_list(files, "data", "mc", tree_name=tree,
                                   expand_files=expand,
                                   confirm_tree=True,
                                   no_empty_files=empty)
    assert "Missing" in str(e) and "events" in str(e)


def test_get_file_list_expander():
    xrootd = fc_write.get_file_list_expander("xrootd")
    assert xrootd is catalogues.XrootdExpander

    local = fc_write.get_file_list_expander("local")
    assert local is catalogues.LocalGlobExpander

    with pytest.raises(RuntimeError) as e:
        fc_write.get_file_list_expander("gobbledy gook")
    assert "Unknown file expander" in str(e)
