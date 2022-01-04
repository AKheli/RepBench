from matplotlib import pyplot as plt
from sklearn import linear_model
import numpy as np
from sklearn.experimental import enable_halving_search_cv  # noqa

from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import Robust_PCA_estimator
from Scenarios.Anomaly_Types import *
from Scenarios.metrics import RMSE
from Scenarios.scenario_types.BaseScenario import BaseScenario
from data_methods.Helper_methods import *

threshold = 2.19

if __name__ == "__main__":
    model = Robust_PCA_estimator(delta=0.061, n_components=3, threshold=threshold, shift=10)
    file_name = searchfile("YAHOO.csv")
    df = get_df_from_file(file_name)[0]
    b = BaseScenario(anomaly_type=DISTORTION)
    results = b.transform_df(df)["full_set"]
    truth = results["original"]
    injected = results["injected"]
    print("eyy",RMSE(truth,injected,[0]))
    plt.plot(injected.iloc[:, 0])
    plt.show()

    truth = truth.drop("class" , axis=1)
    injected = injected.drop("class" , axis=1)
    df = df.drop("class" , axis = 1)
    model.fit(injected.copy())
    reduced_data = pd.DataFrame(model.predict(injected))
    print("RMSE",RMSE(truth,reduced_data,[0]))


    def add_features(shift, window, X):
        shifts = [X.shift(i, fill_value=0) for i in range(shift+1) if i != 0 ]
        window_df = X.rolling(window, min_periods=1).mean()
        return pd.concat([X] + shifts + [window_df], axis=1)


    reduced = pd.DataFrame(model.reduce(injected)).iloc[:,[0]]
    reduced  = add_features(1,10,reduced)
    reduced[2] = np.array(injected.index)




    # plt.plot(reduced[:,0])
    # plt.show()
    for regressor in [ linear_model.HuberRegressor]:
        lr = regressor(epsilon=1.01)
        lr.fit(reduced, injected.iloc[:,0])
        linear_predicted = lr.predict(reduced)
        plt.plot(linear_predicted , label = "linear")
        plt.plot(reduced.iloc[:,0] ,label = "reduced" )
        plt.plot(truth.iloc[:, 0],label = "truth")
        plt.legend()
        plt.show()
        #print(lr.coef_)

        print("RMSE reduced",RMSE(truth,reduced,[0]))
        print("RMSE linear",RMSE(truth,pd.DataFrame(linear_predicted),[0]))

        to_repair_cols = np.array(injected.iloc[:,0].copy())

        diff = linear_predicted - to_repair_cols
        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)

        to_repair_booleans = abs_z_score > threshold

        to_repair_cols[to_repair_booleans] = linear_predicted[to_repair_booleans]
        print("RMSE linear replaced",RMSE(truth,pd.DataFrame(to_repair_cols),[0]))


    print("eyy",RMSE(truth,injected,[0]))


    linear_model.HuberRegressor()
