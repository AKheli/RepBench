import argparse


def add_data_arguments_to_parser(parser):
    parser.add_argument("-data", "-d", nargs=1, type=str, default="None")
    parser.add_argument("-col", "-c", nargs=1, type=str, default=["0"])
    parser.add_argument('-save', nargs="*", type=str, default=False)


def add_injection_arguments_to_parser(parser):
    parser.add_argument('-anomaly_type', '-at', nargs=1, default="amp")
    parser.add_argument("-scenario", nargs=1, type=str, required=True)


def add_repair_arguments_to_parser(parser):
    parser.add_argument("-algo", nargs=1, type=str, required=True)


def init_injection_parser():
    parser = argparse.ArgumentParser()
    add_data_arguments_to_parser(parser)
    add_injection_arguments_to_parser(parser)
    return parser.parse_args()


def init_repair_parser():
    parser = argparse.ArgumentParser()
    add_data_arguments_to_parser(parser)
    add_repair_arguments_to_parser(parser)
    return parser.parse_args()


def init_parser():
    parser = argparse.ArgumentParser()
    add_data_arguments_to_parser(parser)
    add_injection_arguments_to_parser(parser)
    add_repair_arguments_to_parser(parser)
    return parser.parse_args()
