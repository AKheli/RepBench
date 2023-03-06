import itertools

from injection.scenarios.scen_gen import build_scenario
from injection.scenarios.scenario import Scenario
import testing_frame_work.argument_parsers as arg_parser
import testing_frame_work.repair as alg_runner
from injection.scenarios.scenario_saver.Scenario_saver import save_scenario
from testing_frame_work.parameterization import load_params_from_toml
from testing_frame_work.data_methods.data_class import infer_data_file
import injection.injection_config as ic


def main(input=None):
    args = arg_parser.init_checked_parser(input)

    if args.alg is not None:
        algorithms: str = arg_parser.parse_repair_algorithms(args)

    elif args.algx is not None:
        algorithms = arg_parser.parse_repair_algorithms_x(args)

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
            data_paths.append(infer_data_file(file_name, folder="data" + os.sep + "test"))
    else:
        data_paths = [infer_data_file(file_name, folder="data/test") for file_name in test_data_dir]

    data_set_names = [s.split(os.sep)[-1].replace(".csv", "") for s in data_paths]
    print("running on ", data_set_names)
    anomaly_types = arg_parser.parse_anomaly_types(args)
    cols = args.cols
    for (scen_name, data_name, anomaly_type) in itertools.product(scen_names, data_set_names, anomaly_types):
        if scen_name == ic.ANOMALY_SIZE and anomaly_type == ic.POINT_OUTLIER:
            print("skipping anomaly_lenght outlier scenario")
            continue
        try:
            scenario: Scenario = build_scenario(scen_name, data_name, a_type=anomaly_type, data_type="test", cols=cols)
        except Exception as e:
            print(f'Buidling {scen_name} on {data_name} with {anomaly_type} anomalies  failed')
            raise e
        repairer = alg_runner.AnomalyRepairer(1, 1)

        for name, test_part in scenario.name_container_iter:
            for repair_type in algorithms:
                print(f"running repair on {data_name} , {scen_name} with {repair_type} on {anomaly_type} anomalies")
                params = load_params_from_toml(repair_type)
                repair_info = repairer.repair_data_part(repair_type, test_part, params)
            test_part.save(folder="Results/Generated")
    save_scenario(scenario, repair_plot=True, res_name=args.rn)


if __name__ == '__main__':
    main()
