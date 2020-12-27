# plots a distribution of values in a matrix
import logging
from dataclasses import dataclass
from itertools import chain
from pathlib import Path

import matplotlib.pyplot as plt

from .dm_exponent import read_dm
from src.utils import PipelineStepInterface


def plot_hist(input_csv: Path, output_png: Path):
    dm, _ = read_dm(input_csv)
    all_items = list(chain.from_iterable(dm))
    plt.figure()
    plt.hist(all_items)
    plt.title(" distances distribution ")
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png)


@dataclass
class DmHistogramStep(PipelineStepInterface):
    input_csv: Path
    output_png: Path

    def output_exists(self):
        return self.output_png.exists()

    def run(self) -> int:
        try:
            logging.getLogger("matplotlib.font_manager").disabled = True  # suppress matplotlib debug prints
            plot_hist(self.input_csv, self.output_png)
        except Exception as e:
            logging.exception(e)
            return -1
        return 0
