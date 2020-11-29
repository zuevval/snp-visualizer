import logging
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

from src.modules.dm_exponent import read_dm
from src.utils import PipelineStepInterface


@dataclass
class HeatMapStep(PipelineStepInterface):  # TODO add separate test for heatmap
    input_dm_csv: Path
    output_png: Path
    title: str = "heatmap based on the distance matrix"

    def output_exists(self):
        return self.output_png.exists()

    def run(self) -> int:
        try:
            samples_lists, _ = read_dm(self.input_dm_csv)
            samples = np.array(samples_lists).astype(float)
            n = len(samples)
            assert samples.shape == (n, n), "format error: only n*n square matrices allowed"

            logging.getLogger("matplotlib.font_manager").disabled = True  # suppress matplotlib debug prints
            plt.figure()
            plt.imshow(samples, cmap='hot', interpolation='nearest')
            self.output_png.parent.mkdir(parents=True, exist_ok=True)
            plt.title(self.title)
            plt.savefig(self.output_png)
        except Exception as e:
            logging.exception(e)
            return -1
        return 0
