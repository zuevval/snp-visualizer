import json
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from sklearn.manifold import TSNE  # type: ignore

from src.utils import get_out_path


def read_samples_vectors(path: Path) -> Optional[Dict[int, List[int]]]:
    try:
        with open(str(path)) as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def t_sne(json_path: Path, n_dim: int) -> Optional[np.ndarray]:
    samples_dict: Optional[Dict[int, List[int]]] = read_samples_vectors(json_path)
    if not samples_dict:
        print("json not found at path:" + str(json_path))  # TODO logging
        return None
    samples = np.array(list(samples_dict.values()))

    coord: np.ndarray = TSNE(n_components=n_dim).fit_transform(samples)

    return coord


def plot_tsne_2d(coord: np.ndarray, out_filename: str):
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    ax.scatter(coord[:, 0], coord[:, 1], lw=0, s=40)
    out_path = get_out_path() / out_filename
    plt.savefig(out_path)


def plot_tsne_3d(coord: np.ndarray, out_filename: str):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(coord[:, 0], coord[:, 1], coord[:, 2])
    out_path = get_out_path() / out_filename
    plt.savefig(out_path)


def main():
    for json_dir, out_filename in [
        (get_out_path() / "real_data/main/", "tsne_filtered_snps"),
        (get_out_path() / "real_data/no_annotations/", "tsne_all_snps"),
    ]:
        for n_dim in [2, 3]:

            coordinates = t_sne(json_path=json_dir / "samples_vectors.json", n_dim=n_dim)
            np.savetxt(json_dir / ("tsne_coordinates_" + str(n_dim) + "d.txt"), X=coordinates)  # TODO make output param
            if n_dim == 2:
                plot_tsne_2d(coordinates, out_filename + "2d.png")
            else:
                plot_tsne_3d(coordinates, out_filename + "3d.png")


if __name__ == "__main__":
    main()
