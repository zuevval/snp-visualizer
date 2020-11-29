import logging
from dataclasses import dataclass
from pathlib import Path

from Bio import Phylo  # type: ignore
from skbio import DistanceMatrix  # type: ignore
from skbio.tree import nj  # type: ignore
import matplotlib.pyplot as plt  # type: ignore

from src.modules.dm_exponent import read_dm
from src.utils import PipelineStepInterface, safe_w_open


@dataclass
class NjStep(PipelineStepInterface):
    input_dm_csv: Path
    output_dnd: Path
    output_png: Path
    title: str = "neighborhood join tree (based on the distance matrix)"

    def output_exists(self):
        return self.output_png.exists()

    def run(self) -> int:
        try:
            dm, _ = read_dm(self.input_dm_csv)
            newick_tree = nj(DistanceMatrix(dm), result_constructor=str)
            with safe_w_open(self.output_dnd) as dnd_file:
                dnd_file.write(str(newick_tree))

            tree = Phylo.read(self.output_dnd, "newick")

            logging.getLogger("matplotlib.font_manager").disabled = True  # suppress matplotlib debug prints
            plt.figure()
            Phylo.draw(tree, do_show=False)
            plt.title(self.title)

            self.output_png.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(self.output_png)

        except Exception as e:
            logging.exception(e)
            return -1
        return 0
