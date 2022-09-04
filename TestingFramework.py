import itertools

from Scenarios.scenario import Scenario
import testing_frame_work.argument_parsers as arg_parser
import testing_frame_work.repair  as alg_runner
from Scenarios.scenario_generator import build_scenario
from Scenarios.scenario_saver.Scenario_saver import save_scenario
from testing_frame_work.parameterization import load_params_from_toml, params_from_training_set
import numpy as np

def main(input = None):

    args = arg_parser.init_checked_parser(input)

    train_method , train_metric = arg_parser.parse_training_arguments(args)
    train_argument = args.train

    use_training_set = True
    if train_argument == "off":
        use_training_set = False

    algx = False
    if args.alg is not None:
        algorithms : str = arg_parser.parse_repair_algorithms(args)

    elif args.algx is not None:
        algorithms = arg_parser.parse_repair_algorithms_x(args)
        algx = True
        train = False
    else:
        assert False, "algx or alg has to be given as a parameter"


    scen_names = arg_parser.parse_scen_names(args)
    data_files = arg_parser.parse_data_files(args)

    anomaly_types = arg_parser.parse_anomaly_types(args)
    runtime_n = args.run_time_n
    cols = [0]

    print( scen_names, data_files , anomaly_types)
    if not use_training_set:
        for (scen_name, data_name , anomaly_type) in itertools.product(scen_names, data_files , anomaly_types):
            try:
                scenario: Scenario = build_scenario(scen_name,data_name, cols_to_inject=cols,a_type=anomaly_type ,train_test_split = None)
            except Exception as e:
                print(f'running repair on {data_name} with scen type {scen_name} failed')
                raise e
            #print(f'running repair on {data_name} with scen type {scen_name}')
            for repair_type in algorithms:
                for name, train_part, test_part in scenario.name_train_test_iter:
                    params = load_params_from_toml(repair_type)
                    #print("repair with ",repair_type,"params:", params)
                    repair_output = alg_runner.run_repair(repair_type, params, **test_part.repair_inputs,runtime_measurements=runtime_n)
                    test_part.add_repair(repair_output,repair_type)

            save_scenario(scenario, repair_plot=True,  res_name=args.rn)

if __name__ == '__main__':
    main()

