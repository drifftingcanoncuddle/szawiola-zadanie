from Maintain.MainLoop import MainLoop
import sys
from Maintain.Draw import Draw
from Maintain.ConfigManipulator import ConfigManipulator
from Maintain.ConfigManipulator import ConfigFields

def main(argv):
    MainLoop(argv).run()
    # Draw().draw()
    # print(ConfigFields.time.value)


if __name__ == "__main__":
    main(sys.argv[1:])
