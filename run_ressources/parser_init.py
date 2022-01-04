import argparse


def add_data_arguments_to_parser(parser):
    parser.add_argument("-data", "-d", nargs=1, type=str, default=["stock10k.data"])
    parser.add_argument("-col", "-ts", nargs=1, type=str, default=["0"])


def add_injection_arguments_to_parser(parser):
    parser.add_argument('-anomaly_type', '-at', nargs=1, default="amp")
    parser.add_argument("-scenario", nargs=1, type=str,  default="base")
    parser.add_argument("-saveinjected",  action='store_true')


def add_repair_arguments_to_parser(parser):
    parser.add_argument("-algo", nargs=1, type=str, default="all")
    parser.add_argument("-saverepair",  action='store_true')


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


def init_parser(input = None):
    parser = argparse.ArgumentParser()

    add_data_arguments_to_parser(parser)
    add_injection_arguments_to_parser(parser)
    add_repair_arguments_to_parser(parser)
    if input is not None:
        print("EYYYY", input)
        return parser.parse_args(input.split())

    return parser.parse_args()
