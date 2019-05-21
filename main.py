from Maintain.MainLoop import MainLoop
import sys


def main(argv):
    MainLoop(argv).run()


if __name__ == "__main__":
    main(sys.argv[1:])
