import argparse
import sys


def type_convertion(choices, para_name):
    def f(str):
        result = []
        for s in str.split(","):
            if s not in choices:
                sys.tracebacklimit = 0
                raise SystemExit(f'{s} not in possible {para_name} inputs:{choices}')
            result.append(s)
        return result
    return f

def add_data_arguments_to_parser(parser, data_choices):
    parser.add_argument("-data", "-d", type= type_convertion(choices=data_choices, para_name="d"))
    parser.add_argument("-col", "-ts", type=str, default= "0")


def add_injection_arguments_to_parser(parser ,scenario_choices ,anomaly_choices):
    print(scenario_choices)
    parser.add_argument('-a_type','-anom' ,  type=type_convertion(choices=anomaly_choices, para_name="a_type"))
    parser.add_argument("-scenario", "-scen", type=type_convertion(choices=scenario_choices, para_name="scen"))
    parser.add_argument("-saveinjected",  action='store_true')


def add_repair_arguments_to_parser(parser,estimator_choices):
    parser.add_argument("-alg" , type=type_convertion(choices=estimator_choices, para_name="alg"))
    parser.add_argument("-algx", type=str)

    #parser.add_argument("-saverepair",  action='store_true')


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


def init_parser(input = None , estimator_choices = None ,scenario_choices = None , data_choices = None ,anomaly_choices = None):
    parser = argparse.ArgumentParser()

    add_data_arguments_to_parser(parser , data_choices = data_choices)
    add_injection_arguments_to_parser(parser,scenario_choices = scenario_choices , anomaly_choices = anomaly_choices)
    add_repair_arguments_to_parser(parser,estimator_choices = estimator_choices)

    if input is not None:
        "For testing outside of the terminal"
        args = parser.parse_args(input.split())
    else:
        args = parser.parse_args()

    print(args)
    assert args.alg is not None or args.algx is not None, f"alg or algx needs to be defined"
    return args
