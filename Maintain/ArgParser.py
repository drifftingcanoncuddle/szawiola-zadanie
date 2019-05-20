from PyQt5 import QtGui
from PyQt5 import QtWidgets
import argparse


class ArgParser:
    def __init__(self, argv):
        self.parser = None

        self.create_parser()
        self.run_parser(argv)

    def create_parser(self):
        description = "Program created as assignment for Fizyka dla Informatykow. \n" \
                      "It's main task is to evaluate entropy and create proper animation" \
                      "for it."

        epilog = "Project was created by: Piotr Tylczynski, Natalia Czyzewska, Filip Kozlowski"

        self.parser = argparse.ArgumentParser(description=description, epilog=epilog)
        self.parser.add_argument("-f", "--file", dest="data_file", help="File containing set of initial values for simulation")
        self.parser.add_argument("-m", "--microstates", help="Evaluate only microstates", action="store_true")
        self.parser.add_argument("-t", "--thprob", help="Evaluate only thermal probability", action="store_true")
        self.parser.add_argument("-e", "--entropy", help="Evaluate only entropy", action="store_true")
        self.parser.add_argument("-c ", "--chart", dest="location", help="Create chart with entropy and save it to file")
        self.parser.add_argument("-r", "--recreate", help="Recreate default config", action="store_true")
        self.parser.add_argument("-s", "-save", dest="file_name", help="Save result to file")

    def run_parser(self, argv):
        print(self.parser.parse_args(argv))
