from src.tsv_reader import get_significant_snp
from test.testing_utils import prepare_test_data, get_data_path


def test_snp_to_lists():
    snp_info = prepare_test_data()
    assert snp_info.snp_dic == {101: ["1", "10", "10", "rs01", "A", "G"],
                       102: ["1", "21", "21", "rs02", "C", "G"],
                       103: ["1", "35", "35", "rs03", "C", "T"]}
    assert snp_info.snp_indices == {101: 0, 102: 1, 103: 2}
    assert snp_info.snp_ids == [101, 102, 103]
    assert snp_info.samples_vectors == {
        5: [1, 0, 2],
        6: [0, 1, 1],
        7: [2, 2, 1],
        8: [1, 1, 0],
        9: [0, 0, 2]
    }


def test_get_significant_snp():
    assert get_significant_snp(str(get_data_path() / "test/snp_annotation.tsv")) == {103}


def test_snp_to_lists_significant_only():
    snp_info = prepare_test_data(significant_only=True)
    assert snp_info.snp_dic == {103: ["1", "35", "35", "rs03", "C", "T"]}
    assert snp_info.snp_indices == {103: 0}
    assert snp_info.snp_ids == [103]
    assert snp_info.samples_vectors == {
        5: [2],
        6: [1],
        7: [1],
        8: [0],
        9: [2]
    }
