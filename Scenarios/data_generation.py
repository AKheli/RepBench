from Scenarios.data_part import DataPart
from Scenarios.scenario_generator import build_scenario


def full_train_test(data_set,a_type, max_n_rows = 5000):
    screnario = build_scenario("base", data_set, a_type=a_type,max_n_rows=5000)
    for key,val in screnario.part_scenarios.items():
        test_part : DataPart = val
        train_part : DataPart = test_part.train
    return train_part , test_part