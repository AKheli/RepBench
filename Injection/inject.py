import sys

from Scenarios.scenario_types.BaseScenario import BaseScenario
from run_ressources.helpers import split_data_set

sys.path.append('../') # always run from the toplevel folder

def drop_class(data):
    try:
        data = data.drop("class", axis=1)
    except:
        pass
    return data


def get_scenario_data(scenario , data , columns_to_inject ,train_split = 0.2 ):
    """Params
    scen  : Scenario
    data :
    columns_to_inject : list of columns to injected
    train_split : ratio of the data to use for splitting

    Returns:
    dictionary {  scenario_data : { scen_part_name1 : df , ... }
    , train : df , train_class : df}
    """
    base = BaseScenario(scenario.anomaly_type) # to inject the training data
    data = drop_class(data)
    train , test = split_data_set(data,train_split)
    results = {}
    scenario_data = scenario.transform_df(test, cols=columns_to_inject)

    results["scenario_data"] = scenario_data
    if train_split > 0:
        train = list(base.transform_df(train, cols=columns_to_inject).values())[0]
        results["train_class"] = train["class"]
        results["train"] = train["injected"]
        results["train_original"] = train["original"]

    return results


# if __name__ == '__main__':
#     args = init_injection_parser()
#     data_dict = read_data_arguments(args)
#     scenario =  read_injection_arguments(args)
#     cols = data_dict.pop("columns")
#     injected_results = inject(scenario,data_dict=data_dict,columns_to_inject= cols)
#     save_injection_scenario(scenario, injected_results, data_dict)
#
