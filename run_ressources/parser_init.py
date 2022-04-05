import argparse


def add_data_arguments_to_parser(parser, data_choices = None):
    parser.add_argument("-data", "-d", type=str,  choices=data_choices)
    parser.add_argument("-col", "-ts", type=str, default= "0")


def add_injection_arguments_to_parser(parser ,scenario_choises = None):
    parser.add_argument('-a_type','-anom' ,  default="amp" , help="anomaly type")
    parser.add_argument("-scenario", "-scen" ,type=str,  choices=scenario_choises)
    parser.add_argument("-saveinjected",  action='store_true')


def add_repair_arguments_to_parser(parser):
    parser.add_argument("-algo", type=str, default="all")
    parser.add_argument("-algox", type=str, default="")

    parser.add_argument("-saverepair",  action='store_true')


def init_injection_parser(scenario_choises = None):
    parser = argparse.ArgumentParser()
    add_data_arguments_to_parser(parser)
    add_injection_arguments_to_parser(parser , scenario_choises =scenario_choises)
    return parser.parse_args()


def init_repair_parser():
    parser = argparse.ArgumentParser()
    add_data_arguments_to_parser(parser)
    add_repair_arguments_to_parser(parser)
    return parser.parse_args()


def init_parser(input = None , scenario_choises = None , data_choices = None):
    parser = argparse.ArgumentParser()

    add_data_arguments_to_parser(parser , data_choices = data_choices)
    add_injection_arguments_to_parser(parser,scenario_choises = scenario_choises)
    add_repair_arguments_to_parser(parser)

    if input is not None:
        "For testing outside outside of the terminal"
        return parser.parse_args(input.split())

    return parser.parse_args()
