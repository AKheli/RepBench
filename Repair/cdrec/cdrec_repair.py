# import matplotlib.pyplot as plt
# import pandas as pd
# from sklearn.utils import check_array
#
# from Repair.cdrec.recovery import centroid_recovery
# import numpy as np
# import imageio
#
# from Repair.cdrec.recovery2 import centroid_recovery2
# from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
# from Scenarios.scenario_types.BaseScenario import BaseScenario
# from data_methods.Helper_methods import get_df_from_file
# import random
# import os
# number_of_splits = 5
#
#
# def cdrec_repair(injected, cols=[0], **args):
#     injected.plot()
#     plt.show()
#     matrix_injected = check_array(injected, dtype=[np.float32], ensure_2d=True,
#                         copy=True)
#
#     n , m = matrix_injected.shape
#     range_ = np.array_split(np.arange(n),number_of_splits)
#     # np.random.shuffle(range_)
#     # indices =  np.array_split(range_,number_of_splits)
#     filenames = []
#     plt.close()
#     for i in range_:
#         mat_i = matrix_injected.copy()
#         mat_i[i[i>10],cols] = np.nan
#         # recovered_i = pd.DataFrame(centroid_recovery(mat_i.copy()))
#         #
#         # recovered_i2 = pd.DataFrame(centroid_recovery2(mat_i.copy()))
#         a = centroid_recovery(mat_i.copy())
#         b = centroid_recovery2(mat_i.copy())
#
#         assert np.allclose(a,b)
#         print("close")
#         break
#         #recovered_i2 = pd.DataFrame(centroid_recovery2(mat_i))
#         # recovered_i.plot()
#         # plt.axvspan(min(i),max(i), facecolor='b', alpha=0.2)
#         # for j in range(5) :
#         #     filename = f'{min(i)}_{j}.png'
#         #     filenames.append(filename)
#         #     plt.savefig(filename)
#         # plt.close()
#         # #plt.show()
#
#     # # Build GIF
#     # try:
#     #     with imageio.get_writer('mygif0.mp4', mode='I') as writer:
#     #         for filename in filenames:
#     #             image = imageio.imread(filename)
#     #             writer.append_data(image)
#     #
#     # # Remove files
#     # finally:
#     #     for filename in set(filenames):
#     #         os.remove(filename)
#
#     return
#
# def inject(data, anomaly_type):
#     b = BaseScenario(anomaly_type=anomaly_type)
#     injected = b.transform_df(data)["full_set"]["injected"]
#     return injected
#
# def main():
#     truth = get_df_from_file("BAFU.txt")[0]
#     injected = inject(truth,AMPLITUDE_SHIFT)
#     cdrec_repair(injected)
#
#
# if __name__ == "__main__":
#     main()
