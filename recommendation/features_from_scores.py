import os
import sys
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.feature_extraction.load_features import compute_features

load_non_normalized_truth_features = True

load_path = "recommendation/results/scores"
store_path = "recommendation/results/features"
file_name = "results_test" if len(sys.argv) == 1 else sys.argv[1]
store_file_name = "try" # file_name + "_features" + ("_non_normalized" if load_non_normalized_truth_features else "")


print("loading features from " + load_path + "/" + file_name +
      " and storing them in " + store_path + "/" + store_file_name)

compute_features(load_filename=f"{load_path}/{file_name}",
                 store_filename=f"{store_path}/{store_file_name}",use_rawdata=load_non_normalized_truth_features)


