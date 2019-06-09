from Arithmetic.DrawVelocity import DrawVelocity
from Maintain.InputParser import InputParser
from Arithmetic.DrawEntropy import Entropy
from Arithmetic.DrawTHProb import THProb
from Maintain.ConfigManipulator import ConfigManipulator, ConfigFields
from Arithmetic.DrawVX import DrawVX
from simulation.Simulator import Simulator


class MainLoop:
    """
    Joke, it's not loop anymore ;)
    Decides what to do, aka invokes proper functions to accomplish tasks
    given by user
    """
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

        if self.arguments.init_state_file is not None:
            ConfigManipulator().set(ConfigFields.init_state_file,
                                    self.arguments.init_state_file)
        else:
            ConfigManipulator().set(ConfigFields.init_state_file,
                                    "")

        if self.arguments.recreate:
            ConfigManipulator().recreate()

        if self.arguments.thprob:
            THProb().evaluate()

        if self.arguments.entropy:
            Entropy().evaluate()

        if self.arguments.velocity:
            DrawVelocity().evaluate()

        if self.arguments.positions:
            DrawVX().draw()

        if self.arguments.simulation:
            Simulator().dump()

    def show(self, data):
        print(data)
        if len(self.arguments.output_file) > 0:
            with open(self.arguments.output_file, "a") as file:
                file.write(str(data) + "\n")
