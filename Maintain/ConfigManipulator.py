import configparser
from enum import Enum


class ConfigFields(Enum):
    size = "size"
    maxSpeed = "maxSpeed"
    particleAmount = "particleAmount"
    boxSize = "boxSize"
    time = "time"
    timeDelta = "timeDelta"
    init_state_file = "init_state_file"
    particleSize = "particleSize"
    maximalDistanceAsCollision = "maximalDistanceAsCollision"
    maximalTimeDeltaAsColliding = "maximalTimeDeltaAsColliding"


class ConfigManipulator:
    def __init__(self):
        self.config_file_name = "config.ini"
        self.parser = self.create_configreader()

    def create_configreader(self) -> configparser.ConfigParser:
        parser = configparser.ConfigParser()

        try:
            file = open(self.config_file_name, "r")
            file.close()
        except FileNotFoundError as E:
            print(E)
            return self.recreate()

        parser.read(self.config_file_name)

        if "DEFAULT" not in parser:
            return self.recreate()
        else:
            return parser

    def read(self, name: ConfigFields) -> str:
        name = name.value.lower()
        return self.parser["DEFAULT"][name]

    def recreate(self):
        print("Recreating config")
        parser = configparser.ConfigParser()
        parser["DEFAULT"] = {}
        default = parser["DEFAULT"]

        default["size"] = "100"
        default["maxSpeed"] = "50"
        default["particleAmount"] = "100"
        default["boxSize"] = "10"
        default["time"] = "10"
        default["timeDelta"] = "0.01"
        default["init_state_file"] = ""
        default["particleSize"] = "2"
        default["maximalDistanceAsCollision"] = "0.1"
        default["maximalTimeDeltaAsColliding"] = "0.1"
        # default["output_file"] = ""

        self.save_parser_to_file(parser)

        return parser

    def save_parser_to_file(self, parser: configparser.ConfigParser):
        with open(self.config_file_name, "w") as file:
            parser.write(file)

    def set(self, name:str, value):
        self.parser["DEFAULT"][name] = str(value)
        self.save_parser_to_file(self.parser)


