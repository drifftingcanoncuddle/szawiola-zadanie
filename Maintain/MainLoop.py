from Maintain.InputParser import InputParser
from Arithmetic.Microstates import  Microstates
from Arithmetic.Entropy import Entropy
from Arithmetic.EntropyPrinter import EntropyPrinter
from Arithmetic.THProb import THProb
from Maintain.ConfigManipulator import ConfigManipulator


class MainLoop:
    def __init__(self, argv):
        self.argv = argv
        self.arguments = InputParser(argv).get_arguments()
        print(self.arguments)

    def run(self):
        """
        if self.arguments.output_file is not None:
            ConfigManipulator().set("output_file",
                                    self.arguments.output_file)
        """

        if len(self.arguments.output_file) > 0:
            with open(self.arguments.output_file, "w") as file:
                file.write("")

        if self.arguments.sim_time is not None:
            ConfigManipulator().set("time",
                                    self.arguments.sim_time)

        if self.arguments.init_state_file is not None:
            ConfigManipulator().set("init_state_file",
                                    self.arguments.init_state_file)

        if self.arguments.recreate:
            ConfigManipulator().recreate()

        if self.arguments.microstates:
            self.show(Microstates().evaluate())

        if self.arguments.thprob:
            self.show(THProb().evaluate())

        if self.arguments.entropy:
            self.show(Entropy().evaluate())

        if self.arguments.chart_location is not None:
            EntropyPrinter(self.arguments.chart_location)\
                .evaluate()

    def show(self, data):
        print(data)
        if len(self.arguments.output_file) > 0:
            with open(self.arguments.output_file, "a") as file:
                file.write(str(data) + "\n")
