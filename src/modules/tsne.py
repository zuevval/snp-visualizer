import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from sklearn.manifold import TSNE  # type: ignore

from src.utils import get_out_path, PipelineStepInterface


def read_samples_vectors(path: Path) -> Dict[int, List[int]]:
    with open(str(path)) as file:
        return json.load(file)


def t_sne(json_path: Path, n_dim: int) -> Optional[np.ndarray]:
    try:
        samples_dict: Dict[int, List[int]] = read_samples_vectors(json_path)
    except FileNotFoundError:
        logging.exception("json not found at path:" + str(json_path))
        return None
    samples = np.array(list(samples_dict.values()))
    coord: np.ndarray = TSNE(n_components=n_dim).fit_transform(samples)
    return coord


def plot_tsne_2d(coord: np.ndarray, out_path: Path):
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    ax.scatter(coord[:, 0], coord[:, 1], lw=0, s=40)
    plt.savefig(out_path)


def plot_tsne_3d(coord: np.ndarray, out_path: Path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(coord[:, 0], coord[:, 1], coord[:, 2])
    plt.savefig(out_path)


@dataclass
class TSneStep(PipelineStepInterface):
    input_samples_vectors_json: Path
    output_txt: Path
    output_png: Path
    n_dimensions: int

    def output_exists(self):
        return self.output_png.exists() and self.output_txt.exists()

    def run(self) -> int:
        try:
            coordinates = t_sne(json_path=self.input_samples_vectors_json, n_dim=self.n_dimensions)
            self.output_txt.parent.mkdir(parents=True, exist_ok=True)
            np.savetxt(self.output_txt, X=coordinates)

            self.output_png.parent.mkdir(parents=True, exist_ok=True)
            logging.getLogger("matplotlib.font_manager").disabled = True  # suppress matplotlib debug prints
            if self.n_dimensions == 2:
                plot_tsne_2d(coordinates, self.output_png)
            else:
                plot_tsne_3d(coordinates, self.output_png)
        except Exception as e:
            logging.exception(e)
            return -1
        return 0
