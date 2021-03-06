import csv
import json
import logging
from pathlib import Path
from typing import List, Dict, Union, Set
from itertools import islice
from dataclasses import dataclass

from src.utils import safe_w_open, PipelineStepInterface


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


def is_valid_annotation_row(row: List[str], impacts: List[str]) -> bool:
    # expecting data in the format: [snp_id	Consequence	IMPACT]
    impact_idx, row_len = 2, 3
    return (len(row) == row_len) and (row[impact_idx] in impacts)


def get_significant_snp(annotations_filename: str) -> Set[int]:
    modifier = "MODIFIER"
    impacts = ["HIGH", "MODERATE", "LOW", modifier]
    snp_annotations = read_tsv_data(annotations_filename)
    return {int(row[0]) for row in snp_annotations if is_valid_annotation_row(row, impacts) and row[2] != modifier}


@dataclass
class SnpInfo:
    snp_dic: Dict[int, List[str]]  # key: SNP ID, value: SNP info
    snp_ids: List[int]  # list of SNP IDs corresponding to each feature vector
    snp_indices: Dict[int, int]  # key: SNP ID, value: index in sample vector
    samples_vectors: Dict[int, List[int]]  # key: sample ID, value: feature vector


def snp_to_lists(snp_data_filename: str, samples_filename: str, annotations_filename: Union[str, None] = None,
                 max_samples: Union[int, None] = None) -> SnpInfo:
    # reading SNP info (ID, chromosome index, start, end, which nucleotide is replaced, etc)
    snp_data = read_tsv_data(snp_data_filename, skip_header=True)
    snp_dic = {int(row[0]): row[1:] for row in snp_data if is_valid_snp_row(row)}  # key: SNP ID, value: SNP info

    # filtering SNPs by impact (if annotations provided)
    if annotations_filename:
        significant_snp = get_significant_snp(annotations_filename)
        snp_dic = {k: v for k, v in snp_dic.items() if k in significant_snp}

    # reading samples info and converting to feature vectors [x1, x2, ...], xi in {0, 1, 2}, i in {1; len(snp_dic)}
    snp_ids = list(snp_dic.keys())  # list of SNP IDs corresponding to each feature vector
    snp_indices = {key: index for index, key in enumerate(snp_ids)}  # key: SNP ID, value: index in sample vector
    samples = read_tsv_data(samples_filename, max_rows=max_samples, skip_header=True)
    samples_vectors: Dict[int, List[int]] = {}  # key: sample ID, value: feature vector
    for row in samples:
        if len(row) < 3:
            logging.warning("invalid row")
            continue
        sample_id, variant_id, allele_count = [int(x) for x in row]
        if sample_id not in samples_vectors:
            samples_vectors[sample_id] = [0] * len(snp_indices)
        if variant_id in snp_indices:
            samples_vectors[sample_id][snp_indices[variant_id]] = allele_count
    return SnpInfo(snp_dic=snp_dic, snp_ids=snp_ids, snp_indices=snp_indices, samples_vectors=samples_vectors)


@dataclass
class SnpToVectorStep(PipelineStepInterface):
    input_snp_data: Path
    input_samples: Path
    input_annotations: Union[Path, None]

    out_samples_vectors: Path
    out_snp_ids: Path
    out_snp_indices: Path
    out_snp_dic: Path

    def output_exists(self):
        for out_file in [self.out_samples_vectors, self.out_samples_vectors, self.out_snp_indices, self.out_snp_ids]:
            if not out_file.exists():
                return False
        return True

    def run(self) -> int:
        try:
            snp_info = snp_to_lists(snp_data_filename=str(self.input_snp_data),
                                    samples_filename=str(self.input_samples),
                                    annotations_filename=str(self.input_annotations))
            logging.info("loaded " + str(len(snp_info.samples_vectors)) + " samples")

            # dump `snp_info` to json format
            for obj, name in [
                (snp_info.samples_vectors, self.out_samples_vectors),
                (snp_info.snp_ids, self.out_snp_ids),
                (snp_info.snp_indices, self.out_snp_indices),
                (snp_info.snp_dic, self.out_snp_dic),
            ]:
                with safe_w_open(name) as vec_file:
                    vec_file.write(json.dumps(obj))
        except Exception as e:
            logging.exception(e)
            return -1
        return 0
