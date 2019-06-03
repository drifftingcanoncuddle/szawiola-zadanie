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

        epilog = "Project created by: Piotr Tylczynski, Natalia Czyzewska, Filip Kozlowski"

        parser = argparse.ArgumentParser(description=description, epilog=epilog)
        parser.add_argument("-f",
                                 "--file",
                                 dest="init_state_file",
                                 metavar="file",
                                 default="",
                                 help="File containing set of initial values for simulation")

        parser.add_argument("-v",
                                 "--velocity",
                                 help="Show animation of changes in particles velocity",
                                 action="store_true")

        parser.add_argument("-t",
                                 "--thprob",
                                 help="Create animaiton showing changes in thermal probability",
                                 action="store_true")

        parser.add_argument("-e",
                                 "--entropy",
                                 help="Create animation showing changes in entropy",
                                 action="store_true")

        parser.add_argument("-r",
                                 "--recreate",
                                 help="Recreate default config",
                                 action="store_true")

        parser.add_argument("-p",
                                "--positions",
                                help="Create animation showing particle movement in time",
                                action="store_true"
                            )

        parser.add_argument("-s",
                                "--simulation",
                                help="Create new simulation",
                                action="store_true"
                            )

        return parser

    def get_arguments(self) -> argparse.Namespace:
        return self.parser.parse_args(self.argv)



