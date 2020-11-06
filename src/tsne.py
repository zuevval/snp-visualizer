import json
from pprint import pprint
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE

from test.testing_utils import get_out_path


def main():
    with open(str(get_out_path() / "real_data/main/samples_vectors.json")) as file:  # this file is a result of main.py
        samples_dict: Dict[int, List[int]] = json.load(file)
        print("json loaded")
    samples = np.array(list(samples_dict.values()))
    pprint(samples)
    x = TSNE(n_components=2).fit_transform(samples)
    pprint(x)

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    ax.scatter(x[:, 0], x[:, 1], lw=0, s=40)
    plt.savefig(get_out_path() / "plt1.png")


if __name__ == "__main__":
    main()
