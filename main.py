from Maintain.MainLoop import MainLoop
import sys


def main(argv):
    MainLoop(argv).run()
    # Draw().draw()
    # print(ConfigFields.time.value)


if __name__ == "__main__":
    main(sys.argv[1:])
