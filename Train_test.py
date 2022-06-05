import pandas as pd

from Scenarios.Scenario import Scenario
import Repair.algorithms_config as ac
import testing_frame_work.repair  as alg_runner
data = "bafu5k.csv"
a_type = "shift"
error_metrics = [ "mae" , "full_rmse","partial_rmse",  "partial_mutual_info" ,"full_mutual_info"]
train_method = "grid"

alg = ac.RPCA
scenario = Scenario("base",data,a_type=a_type)

train = {}
test =  {}
for error in error_metrics:
    for name, train_part, test_part in scenario.name_train_test_iter:

        params = alg_runner.find_params(alg, metric=error, train_method=train_method,
                                            repair_inputs=train_part.repair_inputs)
        train_scores = alg_runner.run_repair(alg,params,**train_part.repair_inputs)["scores"]
        test_scores =  alg_runner.run_repair(alg,params,**test_part.repair_inputs)["scores"]
        train_scores["params"] = params
        train[error ] = train_scores
        test[error ]  = test_scores

train_df = pd.DataFrame.from_dict(train).T
test_df = pd.DataFrame.from_dict(test).T

print(train_df.to_string())
print(test_df.to_string())