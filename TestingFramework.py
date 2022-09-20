import itertools

from Injection.Scenarios.scen_gen import build_scenario
from Injection.Scenarios.scenario import Scenario
import testing_frame_work.argument_parsers as arg_parser
import testing_frame_work.repair as alg_runner
from Injection.Scenarios.scenario_saver.Scenario_saver import save_scenario
from testing_frame_work.parameterization import load_params_from_toml
from data_methods.data_class import infer_data_file

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

    ### read data file_paths
    data_files = args.data
    import os
    test_data_dir = os.listdir("data/test")
    if "all" not in data_files:
        data_paths = []
        for file_name in data_files:
          data_paths.append(infer_data_file(file_name,folder="data"+os.sep+"test"))

                #raise ValueError(f"{file_name} could not be parsed in data/test:{test_data_dir}")
    else:
        data_paths = [infer_data_file(file_name,folder="data/test") for file_name in test_data_dir]

    data_set_names = [s.split(os.sep)[-1].replace(".csv","") for s in data_paths]
    print("running on ", data_set_names)
    anomaly_types = arg_parser.parse_anomaly_types(args)
    cols = [0]

    for (scen_name, data_name , anomaly_type) in itertools.product(scen_names, data_set_names , anomaly_types):
        try:
            scenario: Scenario = build_scenario(scen_name,data_name,a_type=anomaly_type, data_type="test")
        except Exception as e:
            print(f'running repair on {data_name} with scen type {scen_name} failed')
            raise e

        repairer = alg_runner.AnomalyRepairer(1, 10)
        for repair_type in algorithms:
            for name, test_part in scenario.name_container_iter:
                params = load_params_from_toml(repair_type)
                repairer.repair_data_part(repair_type, test_part,params)

        save_scenario(scenario, repair_plot=True,  res_name=args.rn)

if __name__ == '__main__':
    main()

