import numpy as np
from repair.IMR.IMR_estimator import IMR_estimator
from repair.Screen.screen_estimator import SCREENEstimator
from repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Scenarios.scenario import Scenario
from Scenarios.data_part import DataPart
from parameterization.estimator_optimizer import EstimatorOptimizer
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import Scenarios.ScenarioConfig as sc

sc.MAX_N_ROWS = 5000

#plt.figure(figsize=(, 6), dpi=80)

scen_name = "base"

dataset_names = ["bafu5k.csv", "msd1_5.csv", "elec.csv", "humidity.csv"]
a_types = [ "outlier","shift", "distortion"]


error_metrics = ["full_rmse", "partial_rmse", "mae"]

param_list_dict = {"imr": [{"p": 1, "tau": tau} for tau in np.linspace(0, 0.5, 30)][1:],
                   "screen" : [{"smin": -s, "smax": s} for s in np.linspace(0, 2, 30)[2:]],
                   "rpca" : [{"threshold": t, "classification_truncation": 2} for t in np.linspace(0, 3, 30)[1:]]
                   }

main_param_dict = {"imr": "tau" , "screen" : "smax" , "rpca" : "threshold" } #"classification_truncation"}
estimator_dict = {"imr": IMR_estimator, "screen" : SCREENEstimator , "rpca" : Robust_PCA_estimator }

alg_type = "screen"

pdf = matplotlib.backends.backend_pdf.PdfPages(f"{alg_type}.pdf")


result_string = ""
def min_max(vec):
    return vec
    min_ = min(vec)
    max_ = max(vec)
    if min_ == max_:
        return vec
    diff = max_ - min_
    return [(v - min_) / diff for v in vec]


for error in error_metrics:
    #fig, axs = plt.subplots(1, len(a_types))
    result_string +=error + "\n"

    for ax_index, a_type in enumerate(a_types):
        result_string += a_type + "\n"
        #axis = #axs[ax_index
        axis = plt

        ### one image

        lists = []
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
                                                                            run_time=False)
            x, y = [], []
            main_param = main_param_dict[alg_type]
            for r in res:
                x.append(r[0][main_param])
                y.append(r[1])

            *y, oringinal_rmse_normalized = min_max(y + [oringinal_rmse])
            x, y = zip(*sorted(zip(x, y)))
            axis.plot(x, y, ls="--", marker=".", label=f'{dataset_name[:-4]}' if ax_index == 0 else None)
            # axis.axhline(y=oringinal_rmse, linestyle='-' , label = f"original_error {scen.a_type}")

            lists.append(y)

            result_string += f"{dataset_name}"+ "\n"
            confidence = 0.05
            column = repair_inputs["injected"].iloc[:, 0].values
            result_string += "diff percentile" + str(
            np.percentile(sorted(np.diff(column)), [2.5,97.5])) + "\n"

            trend = np.polyfit(np.arange(len(column)),column, 1)
            #result_string += f"trend {trend[0]}\n"
            result_string += f"optimal found {x[y.index(min(y))]}\n"

        plt.xlabel(main_param)
        tup_list = list(zip(*lists))
        medians = [np.median(t) for t in tup_list]
        min_median = medians.index(min(medians))
        optimal_value = x[min_median]

        print()
        print(error , a_type , "median min ", optimal_value )
        print()
        result_string += "median min, %s %s %f" % (error , a_type , optimal_value ) + "\n"

        import tikzplotlib
        file_name = f"parameter_search/{alg_type}_{error}_{a_type}.txt"
        file_string = tikzplotlib.get_tikz_code()
        file_string = file_string.replace(r"\begin{tikzpicture}",r"\begin{tikzpicture}[scale=\tkscale]")
        if a_type == a_types[0]:
            file_string = file_string.replace(r"\begin{axis}[", r"\begin{axis}["
                                                                r"legend style={at={(2.88,1.23)},legend columns= 4, font = \LARGE, style={column sep=0.5cm}}," )
            file_string = file_string.replace(r"\end{axis}",r"\legend{BAFU, MSD, electricity, humidity}" +"\n" + "\end{axis}")

        file_string = file_string.replace("semithick","unbounded coords=jump")
        with open(file_name, "w") as f:
            f.write(file_string)
        plt.show()

with open(f"parameter_search/{alg_type}_results.txt", "w") as f:
    f.write(result_string)
    # fig.legend()
    # #fig.suptitle(error)
    # fig.tight_layout()
    # pdf.savefig(fig)






pdf.close()
