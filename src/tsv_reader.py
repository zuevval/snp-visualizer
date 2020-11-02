import csv
from typing import List, Tuple, Dict, Any, Union
from collections import defaultdict
from itertools import islice


def read_tsv_data(filename: str, max_rows: Union[None, int] = None, skip_header=False) -> List[List[str]]:
    with open(filename) as fin:
        rd = csv.reader(fin, delimiter="\t")
        if skip_header:
            next(rd)
        if max_rows is None:
            return list(rd)
        else:
            return list(islice(rd, 0, max_rows))


def is_valid_snp_row(row: List[str]) -> bool:
    # expecting data in the format: [id	chr	start	end	rsid	ref	alt], `ref`, `alt` of length 1
    ref_idx, alt_idx, row_len = 5, 6, 7
    return row_len == len(row) and not (len(row[ref_idx]) > 1 or len(row[alt_idx]) > 1)


def snp_to_lists(snp_data_filename: str, samples_filename: str, max_samples: Union[int, None] = None) -> \
        Tuple[Dict[int, List[Any]], Dict[int, int], Dict[int, List[int]]]:
    snp_data = read_tsv_data(snp_data_filename, skip_header=True)
    snp_dic = {int(row[0]): row[1:] for row in snp_data if is_valid_snp_row(row)}
    snp_indices = {key: index for index, key in enumerate(snp_dic.keys())}
    samples = read_tsv_data(samples_filename, max_rows=max_samples, skip_header=True)
    samples_vectors = defaultdict(lambda: [0] * len(snp_indices))
    for row in samples:
        if len(row) < 3:
            print("warning: invalid row")  # TODO set up logger
            continue
        sample_id, variant_id, allele_count = [int(x) for x in row]
        if variant_id in snp_indices:
            samples_vectors[sample_id][snp_indices[variant_id]] = allele_count
    return snp_dic, snp_indices, samples_vectors


def read_snp_annotation(snp_annotation_filename: str):
    pass  # TODO
