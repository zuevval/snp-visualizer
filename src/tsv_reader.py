import csv
from typing import List
from collections import defaultdict


def read_tsv_data(filename: str, skip_header=False) -> List[List[str]]:
    with open(filename) as fin:
        rd = csv.reader(fin, delimiter="\t")
        if skip_header:
            next(rd)
        return list(rd)


def is_valid_snp_row(row: List[str]) -> bool:
    # expecting data in the format: [id	chr	start	end	rsid	ref	alt], `ref`, `alt` of length 1
    ref_idx, alt_idx, row_len = 5, 6, 7
    return row_len == len(row) and not (len(row[ref_idx]) > 1 or len(row[ref_idx]) > 1)


def snp_to_lists(snp_data_filename: str, samples_filename: str):
    snp_data = read_tsv_data(snp_data_filename, skip_header=True)
    snp_dic = {int(row[0]): row[1:] for row in snp_data if is_valid_snp_row(row)}
    snp_indices = {key: index for index, key in enumerate(snp_dic.keys())}
    samples = read_tsv_data(samples_filename, skip_header=True)
    samples_vectors = defaultdict(lambda: [0] * len(snp_indices))
    for row in samples:
        if len(row) < 3:
            print("warning: invalid row")  # TODO set up logger
            continue
        sample_id, variant_id, allele_count = [int(x) for x in row]
        if variant_id in snp_indices:
            samples_vectors[sample_id][snp_indices[variant_id]] = allele_count
    return snp_dic, snp_indices, samples_vectors


def main():
    # from multiprocessing import Pool
    # with Pool(5) as p: # TODO either use multiprocessing, or switch to another language (C++/Java), or both
    #     snp_to_lists("../data/real_data/snp_data.tsv", "../data/real_data/snp2sample.tsv")
    _, _, samples_vectors = snp_to_lists("../data/test/snp_data.tsv", "../data/test/snp2sample.tsv")
    print(samples_vectors)


if __name__ == "__main__":
    main()
