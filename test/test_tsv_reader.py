from test.testing_utils import prepare_test_data


def test_snp_to_lists():
    snp_dic, snp_indices, samples_vectors = prepare_test_data()
    assert snp_dic == {101: ["1", "10", "10", "rs01", "A", "G"],
                       102: ["1", "21", "21", "rs02", "C", "G"],
                       103: ["1", "35", "35", "rs03", "C", "T"]}
    assert snp_indices == {101: 0, 102: 1, 103: 2}
    assert samples_vectors == {
        5: [1, 0, 2],
        6: [0, 1, 1],
        7: [2, 2, 1],
        8: [1, 1, 0],
        9: [0, 0, 2]
    }
