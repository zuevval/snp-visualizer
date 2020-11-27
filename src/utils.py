import logging
import os
from pathlib import Path
from abc import ABCMeta, abstractmethod
from typing import TextIO, List


def _get_path(arg_name: str, default_value: str) -> Path:
    arg_value = Path(os.environ[arg_name]) if arg_name in os.environ else Path(default_value)
    arg_value.mkdir(parents=True, exist_ok=True)
    return arg_value


def get_out_path() -> Path:
    return _get_path("OUT_PATH", "./out")


def get_data_path() -> Path:
    return _get_path("DATA_PATH", "./data")


def get_r_src_path() -> Path:
    return _get_path("R_SRC_PATH", "./src/modules/r/")


def safe_w_open(filename: Path) -> TextIO:
    filename.parent.mkdir(exist_ok=True)
    return open(str(filename), "w")


class PipelineStepInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def output_exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> int:
        raise NotImplementedError


class Pipeline:
    steps: List[PipelineStepInterface]

    def __init__(self, log_filename: Path):
        log_filename.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(handlers=[logging.FileHandler(log_filename), logging.StreamHandler()], level=logging.DEBUG,
                            format="%(asctime)s [%(levelname)s] %(message)s")
        self.steps = []

    def add(self, step: PipelineStepInterface,
            override_existing_output: bool = False):
        if not override_existing_output and step.output_exists():
            msg = "output file(s) for step {} already exist(s)".format(
                type(step).__name__) + " and `override_existing_output` flag is set to false => skipping this step"
            logging.info(msg)
            return
        logging.info("Adding step " + type(step).__name__ + " to pipeline")
        self.steps.append(step)

    def run(self):
        logging.info("starting pipeline run...")
        for step in self.steps:
            logging.info("starting step {}".format(type(step).__name__))
            return_code = step.run()
            logging.info("step {} finished (returned status {})".format(type(step).__name__, return_code))
        logging.info("pipeline exited successfully")
