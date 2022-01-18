from Scenarios.Anomaly_Types import *
import numpy as np

from Injection.injection_methods.basic_injections import  add_anomaly


# def inject_equal_spaced(data, n=10, location="center", anomalies_per_block=1, anomalylength=10,
#                         anomaly_type= AMPLITUDE_SHIFT, blocks="all"):
#     assert anomaly_type in ANOMALY_TYPES, f"anomaly type {anomaly_type} not found , suppoeted are {ANOMALY_TYPES} else modify the injector file"
#
#     data = np.array(data, dtype=np.float64).copy()
#     infos = {}
#     counter = 0
#     results = []
#     for block , array in enumerate(np.array_split(data, n)):
#         if blocks != "all" and block not in blocks:
#             continue
#         for range in [ get_center(len(array))] if location == "center" else get_random_ranges(len(array)
#                 , anom_lenght=anomalylength ,number_of_ranges=anomalies_per_block ):
#             array , info = add_anomaly(anomaly_type, array, range)
#             infos[counter] = info
#         counter += 1
#         results.append(array)
#
#     return np.concatenate(results), infos
