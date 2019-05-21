from PyQt5 import QtGui
from PyQt5 import QtWidgets
import argparse


class InputParser:
    def __init__(self, argv):
        self.argv = argv
        self.parser = self.create_parser()

    def create_parser(self) -> argparse.ArgumentParser:
        description = "Program created as assignment for Fizyka dla Informatykow. \n" \
                      "It's main task is to evaluate entropy and create proper animation" \
                      "for it."

        epilog = "Project was created by: Piotr Tylczynski, Natalia Czyzewska, Filip Kozlowski"

        parser = argparse.ArgumentParser(description=description, epilog=epilog)
        parser.add_argument("-f",
                                 "--file",
                                 dest="init_state_file",
                                 metavar="file",
                                 default="",
                                 help="File containing set of initial values for simulation")

        parser.add_argument("-m",
                                 "--microstates",
                                 help="Evaluate microstates",
                                 action="store_true")

        parser.add_argument("-t",
                                 "--thprob",
                                 help="Evaluate thermal probability",
                                 action="store_true")

        parser.add_argument("-e",
                                 "--entropy",
                                 help="Evaluate entropy",
                                 action="store_true")

        parser.add_argument("-c ",
                                 "--chart",
                                 metavar="file",
                                 dest="chart_location",
                                 help="Create chart with entropy and save it to file")

        parser.add_argument("-r",
                                 "--recreate",
                                 help="Recreate default config",
                                 action="store_true")

        parser.add_argument("-s",
                                 "--save",
                                 dest="output_file",
                                 metavar="file",
                                 default="",
                                 help="Save result to file")

        parser.add_argument("-T",
                                 "--Time",
                                 dest="sim_time",
                                 metavar="time",
                                 help="Set period time of simulation in seconds")

        return parser

    def get_arguments(self) -> argparse.Namespace:
        return self.parser.parse_args(self.argv)



