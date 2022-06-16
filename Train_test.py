import pandas as pd

from Scenarios.Scenario import Scenario
import Repair.algorithms_config as ac
import testing_frame_work.repair  as alg_runner
import time
import matplotlib.pyplot as plt
data = "bafu5k.csv"
a_type = "outlier"
error_metrics = [ "mae" , "full_rmse","partial_rmse"]#,  "partial_mutual_info" ,"full_mutual_info"]

algs = [ac.IMR, ac.SCREEN  ,ac.RPCA , ac.CDREC ]
scenario = Scenario("base",data,a_type=a_type)

file_object = open('score_method.txt', 'r+')
file_object.truncate()
file_object.close()


for error in error_metrics:
    for alg in algs:
        for train_method in ["halving", "bayesian", "grid"]:
            start = time.time()
            for name, train_part, test_part in scenario.name_train_test_iter:
                params = alg_runner.find_params(alg, metric=error, train_method=train_method,
                                        repair_inputs=train_part.repair_inputs)
                train_scores = alg_runner.run_repair(alg,params,**train_part.repair_inputs)["scores"]
                test_scores =  alg_runner.run_repair(alg,params,**test_part.repair_inputs)["scores"]

            file_object = open('score_method.txt', 'a')
            file_object.write(f"{error},{alg},{train_method}\n")
            file_object.write(f"{time.time() - start}\n")
            file_object.write(f"{train_scores}\n")
            file_object.write(f"{test_scores}\n")
            file_object.close()



print(list(scenario.name_train_test_iter))
for error in error_metrics:
    train = {}
    test = {}
    time_dict = {}
    param_dict = {}
    for alg in algs:
        start = time.time()
        for name, train_part, test_part in scenario.name_train_test_iter:
            params = alg_runner.find_params(alg, metric=error, train_method=train_method,
                                    repair_inputs=train_part.repair_inputs)
            train_scores = alg_runner.run_repair(alg,params,**train_part.repair_inputs)["scores"]
            test_scores =  alg_runner.run_repair(alg,params,**test_part.repair_inputs)["scores"]
            train[alg] = {k:abs(v) for k,v in train_scores.items()}
            test[alg]  = {k:abs(v) for k,v in test_scores.items()}
            time_dict[alg] = [time.time()  - start]
            param_dict[alg] = params

    param_df =   pd.DataFrame.from_dict(param_dict)
    time_df =    pd.DataFrame.from_dict(time_dict)
    test_df =    pd.DataFrame.from_dict(test)
    train_df =   pd.DataFrame.from_dict(train)
    test_df.to_csv(path_or_buf=f"TrainResults/{error}_{a_type}_{train_method}_train",index=True,index_label="error")
    train_df.to_csv(path_or_buf=f'TrainResults/{error}_{a_type}_{train_method}_test',index=True,index_label="error")
    time_df.to_csv(path_or_buf=f'TrainResults/{error}_{a_type}_{train_method}_time',index=True,index_label="time")
    param_df.to_csv(path_or_buf=f'TrainResults/{error}_{a_type}_{train_method}_params',index=True,index_label="params")

    # max_values = max(train_df.max().max(),test_df.max().max())
    # ax = train_df.plot.bar(ylim=(0,max_values+0.1))
    # test_df.plot.bar(ax=ax, alpha=0.5 , title = f"trained on {error}")
    # plt.show()


