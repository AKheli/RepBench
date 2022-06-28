import numpy as np
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.screen_estimator import SCREENEstimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Scenarios.Scenario import Scenario
from Scenarios.data_part import DataPart
from parameter_search.estimator_optimizer import EstimatorOptimizer
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from termcolor import colored
import Scenarios.ScenarioConfig as sc

sc.MAX_N_ROWS = 5000

plt.figure(figsize=(25, 6), dpi=80)


scen_name = "base"

dataset_names = ["bafu5k.csv", "msd1_5.csv", "elec.csv", "humidity.csv"]
a_types = ["shift", "outlier", "distortion"]


error_metrics = ["full_rmse", "partial_rmse", "mae"]

param_list_dict = {"imr": [{"p": 1, "tau": tau} for tau in np.linspace(0, 0.5, 100)][1:],
                   "screen" : [{"smin": -s, "smax": s} for s in np.linspace(0, 2, 100)],
                   "rpca" : [{"threshold": t, "classification_truncation": 2} for t in np.linspace(0, 3, 100)[1:]]
                   }

main_param_dict = {"imr": "tau" , "screen" : "smax" , "rpca" : "threshold" } #"classification_truncation"}
estimator_dict = {"imr": IMR_estimator, "screen" : SCREENEstimator , "rpca" : Robust_PCA_estimator }

alg_type = "rpca"

pdf = matplotlib.backends.backend_pdf.PdfPages(f"{alg_type}.pdf")

def min_max(vec):
    min_ = min(vec)
    max_ = max(vec)
    if min_ == max_:
        return vec
    diff = max_ - min_
    return [(v - min_) / diff for v in vec]


for error in error_metrics:
    fig, axs = plt.subplots(1, len(a_types))
    for ax_index, a_type in enumerate(a_types):
        axis = axs[ax_index]

        ### one image

        list_sum = []
        mins = []
        for dataset_name in dataset_names:
            scen = Scenario(scen_name=scen_name, data=dataset_name, a_type=a_type)
            for name, part_scen in scen.part_scenarios.items():
                train_part: DataPart = part_scen.train
                repair_inputs = train_part.repair_inputs
                oringinal_rmse = train_part.original_scores[error]

            estimator = estimator_dict[alg_type]()
            param_list = param_list_dict[alg_type]

            res = EstimatorOptimizer(estim=estimator, error_score=error).param_map(repair_inputs, param_list,
                                                                            run_time=True)
            x, y = [], []
            main_param = main_param_dict[alg_type]
            for r in res:
                x.append(r[0][main_param])
                y.append(r[1])

            *y, oringinal_rmse_normalized = min_max(y + [oringinal_rmse])
            x, y = zip(*sorted(zip(x, y)))
            axis.plot(x, y, ls="--", marker=".", label=f'{dataset_name[:-4]}' if ax_index == 0 else None)
            # axis.axhline(y=oringinal_rmse, linestyle='-' , label = f"original_error {scen.a_type}")
            list_sum = y if len(list_sum) == 0 else [ y1+y2 for y1,y2 in zip(y,list_sum)]

            mins.append(round(x[y.index(min(y))],3))
        axis.set_title(a_type)
        min_index = list_sum.index(min(list_sum))
        optimal_value = x[min_index]
        axis.set(xlabel=f'{main_param} \n min at {round(optimal_value,3)}\n'
                        f' individual:\n  {mins}')
    fig.legend()
    fig.suptitle(error)
    fig.tight_layout()
    pdf.savefig(fig)

    import tikzplotlib
    tikzplotlib.save("mytikz.tex")

    plt.show()



pdf.close()
