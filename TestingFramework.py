import itertools

from Scenarios.Scenario import Scenario
import testing_frame_work.argument_parsers as arg_parser
import testing_frame_work.repair  as alg_runner
from Scenarios.scenario_saver.Scenario_saver import save_scenario


def main(input = None):
    args = arg_parser.init_checked_parser(input)

    if args.alg is not None:
        algorithms = arg_parser.parse_repair_algorithms(args)

    scen_names = arg_parser.parse_scen_names(args)
    data_files = arg_parser.parse_data_files(args)
    anomaly_types = arg_parser.parse_anomaly_types(args)
    train_method , train_metric = arg_parser.parse_training_arguments(args)

    cols = [0]
    #initialize all scenarios first to check if the can be created

    # for i in range(10):
    #     l = []
    #     for (scen_name, data_name , anomaly_type) in itertools.product(scen_names, data_files , anomaly_types):
    #         #print(f'running repair on {data_name} with scen type {scen_name} , anomaly_type {anomaly_type}')
    #         scenario : Scenario = Scenario(scen_name,data_name, cols_to_inject=cols,a_type=anomaly_type)
    #         for name, train_part, test_part in scenario.name_train_test_iter:
    #             hash_ =  train_part.hash()
    #             l.append(hash_)
    #             print(hash_)
    #             if i>0:
    #                 if hash_ not in l:
    #                     print("DAAAAAAAAAAMN",scen_name, data_name , anomaly_type)
    #                     assert False, (scen_name, data_name , anomaly_type)
    #

    #

    for (scen_name, data_name , anomaly_type) in itertools.product(scen_names, data_files , anomaly_types):
        try:
            scenario: Scenario = Scenario(scen_name,data_name, cols_to_inject=cols,a_type=anomaly_type)
        except Exception as e:
            print(f'running repair on {data_name} with scen type {scen_name} failed')
            raise e
        print(f'running repair on {data_name} with scen type {scen_name}')

        for repair_type in algorithms:
             for name, train_part, test_part in scenario.name_train_test_iter:
                store_name = f"{scen_name}_{anomaly_type}_{data_name}_{train_method}_{train_metric}"
                train_hash = train_part.hash(train_method+train_metric)
                params = "default"
                import matplotlib.pyplot as plt
                # train_part.injected.iloc[:, 0].plot()
                # plt.show()
                # try:
                #     params = alg_runner.load_train(repair_type,store_name,id=train_hash)
                #     print("PARAMS ALGREADY COMPUTED")
                # except:
                #     params = alg_runner.find_params(repair_type , metric = train_metric , train_method=train_method , repair_inputs=train_part.repair_inputs , store=store_name,id = train_hash)
                # print(params)
                repair_output = alg_runner.run_repair(repair_type,params, **test_part.repair_inputs)
                test_part.add_repair(repair_output,repair_type)

        save_scenario(scenario, repair_plot=True,  res_name=args.rn)


if __name__ == '__main__':
    main()

