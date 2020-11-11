import json
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from sklearn.manifold import TSNE  # type: ignore

from test.testing_utils import get_out_path


def read_samples_vectors(path: Path) -> Optional[Dict[int, List[int]]]:
    try:
        with open(str(path)) as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def t_sne(json_path: Path, out_filename: str) -> Optional[np.ndarray]:
    samples_dict: Optional[Dict[int, List[int]]] = read_samples_vectors(json_path)
    if not samples_dict:
        print("json not found at path:" + str(json_path))  # TODO logging
        return None
    samples = np.array(list(samples_dict.values()))

    coord: np.ndarray = TSNE(n_components=2).fit_transform(samples)

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    ax.scatter(coord[:, 0], coord[:, 1], lw=0, s=40)
    out_path = get_out_path() / out_filename
    plt.savefig(out_path)
    return coord


def main():
    for json_dir, out_filename in [
        (get_out_path() / "real_data/main/", "tsne_filtered_snps.png"),
        (get_out_path() / "real_data/no_annotations/", "tsne_all_snps.png"),
    ]:
        coordinates = t_sne(json_path=json_dir / "samples_vectors.json", out_filename=out_filename)
        np.savetxt(json_dir / "tsne_coordinates_2d.txt", X=coordinates)


if __name__ == "__main__":
    main()
