import json


folder = "parameterization_results/"
file_name = "rpca_shift_full_rmse.json"


d : dict
with open(folder+file_name) as f:
    d = json.load(f)

for dataset, value in d.items():
    print(value)
    bayesian_scores , *grid_search_scores = value
    print(bayesian_scores)
    print(len(grid_search_scores))
