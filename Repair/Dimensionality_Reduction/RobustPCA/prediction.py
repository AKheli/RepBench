# import numpy as np
#
# def predict(matrix,C,anomaly_matrix = None,call_back_object=None):
#
#     if anomaly_matrix is None:
#         anomaly_matrix = np.isnan(matrix)
#
#
#     X = matrix.copy()
#     X_reduced = reduce(X)
#
#
#     for col in self.columns_to_repair:
#             to_repair_booleans = anomalies[col].copy()
#             i = 1
#             while i < len(to_repair_booleans):
#                 if to_repair_booleans[i]:
#                     last_clean_pont = i - 1
#                     while to_repair_booleans[i]:
#                         i = i + 1
#                     next_clean_pont = i
#                     to_reduce[last_clean_pont + 1:next_clean_pont, col] \
#                         = np.linspace(to_reduce[last_clean_pont, col], to_reduce[next_clean_pont, col],
#                                       next_clean_pont - last_clean_pont - 1)
#                 else:
#                     i = i + 1
#                     # anomaly_found
#
#     # replace with the reduced data
#     X_reduced = self.reduce(to_reduce)
#     for col in self.columns_to_repair:
#         reduced_col = X_reduced[:, col]
#         self.reduced = reduced_col
#         X_copy[anomalies[col], col] = reduced_col[anomalies[col]]
#
#     return X_copy