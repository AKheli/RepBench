from Repair.Robust_PCA import loss
from Repair.Robust_PCA.PCA_algorithms import reconstuct
from Repair.Robust_PCA.m_est_rpca import MRobustPCA
from Repair.res.timer import Timer
import pandas as pd
import numpy as np

def add_feaure(df , shift = 0 , time = False ):
    original_cols = list(df.columns)

    if shift != 0:
        shift = df.shift(periods=shift, fill_value=0)
        shift.columns = [ f'{x}_shift{shift}' for x in original_cols ]
        df = pd.concat([df,shift] , axis = 1)

    if time:
        df["time"] = np.array(df.index)

    return df


def RPCA4(injected, n_components=1, cols=0, threshold=1.5, return_reconstructed=False, **kwargs):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    result = injected.copy()
    # injected.plot()
    timer = Timer()
    timer.start()
    M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.00001))
    sampled = injected.sample(n=300, axis='rows', replace=True)
    M_rpca.fit(sampled)
    Repair_reconstructed = reconstuct(injected, M_rpca)

    for col in cols:
        reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
        to_repair_cols = np.array(injected.iloc[:, col])

        diff = reconstructed_cols - to_repair_cols

        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)

        to_repair_booleans = abs_z_score > threshold

        to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
        result.iloc[:, col] = to_repair_cols


    return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}


def RPCA5(injected, n_components=1, cols=0, threshold=1.5, return_reconstructed=False, **kwargs):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    result = injected.copy()
    injected = add_feaure(injected,time=True)
    timer = Timer()
    timer.start()
    M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.00001))
    sampled = injected.sample(n=300, axis='rows', replace=True)
    M_rpca.fit(sampled)
    Repair_reconstructed = reconstuct(injected, M_rpca)

    for col in cols:
        reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
        to_repair_cols = np.array(injected.iloc[:, col])

        diff = reconstructed_cols - to_repair_cols

        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)

        to_repair_booleans = abs_z_score > threshold

        to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
        result.iloc[:, col] = to_repair_cols

    return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}


def RPCA6(injected, n_components=1, cols=0, threshold=1.5, return_reconstructed=False, **kwargs):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    result = injected.copy()
    injected = add_feaure(injected,shift=1)
    timer = Timer()
    timer.start()
    M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.00001))
    sampled = injected.sample(n=300, axis='rows', replace=True)
    M_rpca.fit(sampled)
    Repair_reconstructed = reconstuct(injected, M_rpca)

    for col in cols:
        reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
        to_repair_cols = np.array(injected.iloc[:, col])

        diff = reconstructed_cols - to_repair_cols

        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)

        to_repair_booleans = abs_z_score > threshold

        to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
        result.iloc[:, col] = to_repair_cols

    return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}

def RPCA6(injected, n_components=1, cols=0, threshold=1.5, return_reconstructed=False, **kwargs):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    result = injected.copy()
    injected = add_feaure(injected,shift=2)
    timer = Timer()
    timer.start()
    M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.00001))
    sampled = injected.sample(n=300, axis='rows', replace=True)
    M_rpca.fit(sampled)
    Repair_reconstructed = reconstuct(injected, M_rpca)

    for col in cols:
        reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
        to_repair_cols = np.array(injected.iloc[:, col])

        diff = reconstructed_cols - to_repair_cols

        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)

        to_repair_booleans = abs_z_score > threshold

        to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
        result.iloc[:, col] = to_repair_cols

    return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}

def RPCA7(injected, n_components=1, cols=0, threshold=1, return_reconstructed=False, **kwargs):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    result = injected.copy()
    injected = add_feaure(injected,shift=1)
    timer = Timer()
    timer.start()
    M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.00001))
    sampled = injected.sample(n=300, axis='rows', replace=True)
    M_rpca.fit(sampled)
    Repair_reconstructed = reconstuct(injected, M_rpca)

    for col in cols:
        reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
        to_repair_cols = np.array(injected.iloc[:, col])

        diff = reconstructed_cols - to_repair_cols

        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)

        to_repair_booleans = abs_z_score > threshold

        to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
        result.iloc[:, col] = to_repair_cols

    return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}



#
# def RPCA4(injected, n_components=2, cols=0, threshold=1.5, return_reconstructed=False, **kwargs):
#     try:
#         injected = injected.drop("class", axis=1)
#     except:
#         pass
#
#     result = injected.copy()
#     # injected.plot()
#     timer = Timer()
#     timer.start()
#     injected = add_shift(injected, 5)
#     injected["time"] = np.array(injected.index)
#
#     M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.00001))
#     sampled = injected.sample(n=300, axis='rows', replace=True)
#     M_rpca.fit(sampled)
#     Repair_reconstructed = reconstuct(injected, M_rpca)
#
#     for col in cols:
#         reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
#         to_repair_cols = np.array(injected.iloc[:, col])
#
#         diff = reconstructed_cols - to_repair_cols
#
#         mean = np.mean(diff)
#         std = np.std(diff)
#         abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)
#
#         to_repair_booleans = abs_z_score > threshold
#
#         to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
#         result.iloc[:, col] = to_repair_cols
#
#     # Repair_reconstructed.iloc[:, cols].plot()
#     # plt.title("reconstructed")
#     # result.plot()
#     # plt.title("result")
#     # plt.show()
#
#     return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}
#
#
# #
# # def RPCA5(injected, n_components=2, cols=0, threshold=1.5, return_reconstructed=False, **kwargs):
# #     try:
# #         injected = injected.drop("class", axis=1)
# #     except:
# #         pass
# #
# #     result = injected.copy()
# #     # injected.plot()
# #     timer = Timer()
#     timer.start()
#     injected = add_shift(injected, 5)
#     injected["time"] = np.array(injected.index)
#
#     M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.00001))
#     sampled = injected.sample(n=300, axis='rows', replace=True)
#     M_rpca.fit(sampled)
#     Repair_reconstructed = reconstuct(injected, M_rpca)
#
#     for col in cols:
#         reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
#         to_repair_cols = np.array(injected.iloc[:, col])
#
#         diff = reconstructed_cols - to_repair_cols
#
#         mean = np.mean(diff)
#         std = np.std(diff)
#         abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)
#
#         to_repair_booleans = abs_z_score > threshold
#
#         to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
#         result.iloc[:, col] = to_repair_cols
#
#     # Repair_reconstructed.iloc[:, cols].plot()
#     # plt.title("reconstructed")
#     # result.plot()
#     # plt.title("result")
#     # plt.show()
#
#     return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}
#
#
# #
# #
# # def RPCA5(injected, n_components=1, cols=0, threshold=1, return_reconstructed=False, **kwargs):
# #     """
# #     uses the whole train to calculate threshold and refits on normal set
# #     """
# #     try:
# #         injected = injected.drop("class", axis=1)
# #     except:
# #         pass
# #     timer = Timer()
# #     timer.start()
# #     oricinal_cols = list(injected.columns)
# #     medians = injected.expanding(5).median()
# #     medians = medians.fillna(0)
# #     medians.columns = [f'{o}_expaned' for o in oricinal_cols]
# #     injected = pd.concat([injected, medians], axis=1)
# #     M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.01))
# #     sampled = injected.sample(n=300, axis='rows', replace=True)
# #     M_rpca.fit(sampled)
# #     Repair_reconstructed = reconstuct(injected, M_rpca)
# #
# #     result = injected.copy()
# #     for col in cols:
# #         reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
# #         to_repair_cols = np.array(injected.iloc[:, col])
# #
# #         diff = reconstructed_cols - to_repair_cols
# #
# #         mean = np.mean(diff)
# #         std = np.std(diff)
# #         abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)
# #
# #         to_repair_booleans = abs_z_score > threshold
# #
# #         to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
# #         result.iloc[:, col] = to_repair_cols
# #
# #     print(M_rpca.components_)
# #
# #     return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}
# #
#
# def RPCA6(injected, n_components=3, cols=0, threshold=1, return_reconstructed=False, **kwargs):
#     """
#     uses the whole train to calculate threshold and refits on normal set
#     """
#     try:
#         injected = injected.drop("class", axis=1)
#     except:
#         pass
#     timer = Timer()
#     timer.start()
#     oricinal_cols = list(injected.columns)
#     medians = injected.expanding(5).median()
#     medians = medians.fillna(0)
#     medians.columns = [f'{o}_expaned' for o in oricinal_cols]
#     injected = pd.concat([injected, medians], axis=1)
#     M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.01))
#     sampled = injected.sample(n=300, axis='rows', replace=True)
#     M_rpca.fit(sampled)
#     Repair_reconstructed = reconstuct(injected, M_rpca)
#
#     result = injected.copy()
#     for col in cols:
#         reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
#         to_repair_cols = np.array(injected.iloc[:, col])
#
#         diff = reconstructed_cols - to_repair_cols
#
#         mean = np.mean(diff)
#         std = np.std(diff)
#         abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)
#
#         to_repair_booleans = abs_z_score > threshold
#
#         to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
#         result.iloc[:, col] = to_repair_cols
#
#     # Repair_reconstructed.plot()
#     # result.plot()
#     # plt.title("pca")
#     # plt.show()
#     return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}
#
# def RPCA7(injected, n_components=1, cols=0, threshold=0.5, return_reconstructed=False, **kwargs):
#     """
#     uses the whole train to calculate threshold and refits on normal set
#     """
#     try:
#         injected = injected.drop("class", axis=1)
#     except:
#         pass
#     timer = Timer()
#     timer.start()
#     oricinal_cols = list(injected.columns)
#     medians = injected.expanding(5).median()
#     medians = medians.fillna(0)
#     medians.columns = [f'{o}_expaned' for o in oricinal_cols]
#     injected = pd.concat([injected, medians], axis=1)
#     M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.01))
#     sampled = injected.sample(n=300, axis='rows', replace=True)
#     M_rpca.fit(sampled)
#     Repair_reconstructed = reconstuct(injected, M_rpca)
#
#     result = injected.copy()
#     for col in cols:
#         reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
#         to_repair_cols = np.array(injected.iloc[:, col])
#
#         diff = reconstructed_cols - to_repair_cols
#
#         mean = np.mean(diff)
#         std = np.std(diff)
#         abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)
#
#         to_repair_booleans = abs_z_score > threshold
#
#         to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
#         result.iloc[:, col] = to_repair_cols
#
#     # Repair_reconstructed.plot()
#     # result.plot()
#     # plt.title("pca")
#     # plt.show()
#
#
#
#     return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}
#
# def RPCA6(injected, n_components=1, cols=0, threshold=0.5, return_reconstructed=False, **kwargs):
#     print("6")
#     """
#     uses the whole train to calculate threshold and refits on normal set
#     """
#     try:
#         injected = injected.drop("class", axis=1)
#     except:
#         pass
#     timer = Timer()
#     timer.start()
#     oricinal_cols = list(injected.columns)
#     medians = injected.expanding(5).median()
#     medians = medians.fillna(0)
#     medians.columns = [f'{o}_expaned' for o in oricinal_cols]
#     injected = pd.concat([injected, medians], axis=1)
#     M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.01))
#     M_rpca.col = len(oricinal_cols)
#     sampled = injected.sample(n=300, axis='rows', replace=True)
#     M_rpca.fit(sampled)
#     Repair_reconstructed = reconstuct(injected, M_rpca)
#
#     result = injected.copy()
#     for col in cols:
#         reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
#         to_repair_cols = np.array(injected.iloc[:, col])
#
#         diff = reconstructed_cols - to_repair_cols
#
#         mean = np.mean(diff)
#         std = np.std(diff)
#         abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)
#
#         to_repair_booleans = abs_z_score > threshold
#
#         to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
#         result.iloc[:, col] = to_repair_cols
#
#     # Repair_reconstructed.plot()
#     # result.plot()
#     # plt.title("pca")
#     # plt.show()
#
#
#
#     return {"repair": result, "PCA_reconstructed": Repair_reconstructed, "runtime": timer.get_time()}
#
#
# #
# # def RPCA4(injected, n_components=1, cols=0, threshold=1, return_reconstructed=False, **kwargs):
# #     """
# #     uses the whole train to calculate threshold and refits on normal set
# #     """
# #     try:
# #         injected = injected.drop("class", axis=1)
# #     except:
# #         pass
# #     timer = Timer()
# #     timer.start()
# #
# #     injected = add_shift(injected,5)
# #     M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.01))
# #     sampled = injected.sample(n=300,axis='rows',replace=True)
# #     M_rpca.fit(sampled )
# #     Repair_reconstructed = reconstuct(injected, M_rpca)
# #
# #     result = injected.copy()
# #     for col in cols:
# #         reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
# #         to_repair_cols = np.array(injected.iloc[:, col])
# #
# #         diff = reconstructed_cols - to_repair_cols
# #
# #         mean = np.mean(diff)
# #         std = np.std(diff)
# #         abs_z_score = diff*0 if std == 0 else abs((diff - mean) / std)
# #
# #         to_repair_booleans = abs_z_score > threshold
# #
# #         to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
# #         result.iloc[:, col] = to_repair_cols
# #
# #     # Repair_reconstructed.plot()
# #     # result.plot()
# #     # plt.title("pca")
# #     # plt.show()
# #
# #     return {"repair": result, "PCA_reconstructed": Repair_reconstructed , "runtime": timer.get_time()}
