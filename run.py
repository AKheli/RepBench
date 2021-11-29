# import argparse
# import numpy as np
#
# parser = argparse.ArgumentParser()
# parser.add_argument("-data","-d" ,nargs=1, type=str , default="")
# parser.add_argument("-anomaly_type","-at" ,nargs=1, type=str , default="")
# parser.add_argument('-algo',   nargs=1, default=[])
# parser.add_argument('-algox',nargs=1, default=[])
# parser.add_argument('-scenario',nargs=1, default=["simple"])
#
# parser.add_argument('-save',  nargs="*", type=str , default=True )
#
# args = parser.parse_args()
#
# files = args.data[0]
from Helper_methods import searchfiles, get_df_from_file
from Repair.repair_algos.Robust_PCA.PCA_algorithms import *
from Repair.repair_algos.repair_algos import IMR_repair
from Scenarios.Scenario import BaseScenario

file_names= "humidity.csv,temp.csv,YAHOO.csv"
files = searchfiles(file_names)

col = 0
results = []
for file in files:
    df , name = get_df_from_file(file)
    split = int(len(df[df.columns[0]])/2)
    train , test = df.iloc[:split,:] , df.iloc[split:,:]

    for i in range(10):
        scenario = BaseScenario(test,col = col)
        injected_dfs_info_test = scenario.get_injected_data()
        scenario = BaseScenario(train , col = col)
        injected_dfs_info_train = scenario.get_injected_data()

        for test_ , train_ in zip(injected_dfs_info_test,injected_dfs_info_train):
            train_df = train_["data"]
            test_df  =  test_["data"]
            truth = test_["truth"]
            injected  = test_df.iloc[:,col]

            test_df["class"] = np.array( truth !=  injected , dtype=int)
            print(sum(test_df["class"]))
            results.append(f'{"injected"} {rmse(truth, injected)}')
            plt.plot(i, [rmse(truth, injected)], color="grey", marker= "_", label = "original" ,markersize = 54)
            #todo save approprietly
            repair_ = IMR_repair(injected,truth)
            repair = repair_["repair"]
            labels = repair_["labels"]
            plt.plot(i, rmse(truth, repair,labels), color="Yellow", label=IMR_repair.__name__, marker="s", markersize=20)

            for rpca ,color , j in zip([RPCA1,RPCA2,RPCA3 , PCA, RPCA4], ["red","blue","green", "black", "orange"], range(5)):
                repair = rpca(test_df, train_df,n_components=2)
                results.append(f'{rpca.__name__} { rmse(truth,repair)}')
                plt.plot(i+j*0.1 , rmse(truth,repair) , color = color,label = rpca.__name__ , marker = "s" , markersize = 20)
                if i == 0:
                    plt.legend()

    plt.show()

print(results)
#
# for file in files_from_comma_string(files):
#     print("trying to init dataframe")
#     df = get_df_from_file(file)
#     print("df" , df)
#     try:
#         data = anom_dict_from_json(file)
#         labels = [0, 1, 2]
#         for anom in data.values():
#             print(anom)
#             labels += anom["index_range"][0:min(3, len(anom["index_range"]))]
#         labels = np.concatenate((labels, np.random.randint(0, high=len(df["truth"]), size=15)), axis=None)
#     except:
#         print("no marked anomaly start found for IMR random labels assigned")
#         labels = np.random.randint(0, high=len(df["truth"]),size= int(len(df["truth"])/15))
#         pass
#
#     for i in args.algo:
#         algos = [{"name": alg, "multiple_algos": {}} for alg in i.split(",")]
#
#         eval = evaluate_from_df(df, algos = algos , labels= labels)
#         print("eval" ,eval)
#
#     for i in args.algox:
#         print(i)
#         eval = evaluate_from_df(df,paramfile = i, labels= labels)
#
#
