import numpy as np
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.screen_estimator import SCREENEstimator
from Scenarios.Scenario import Scenario
from Scenarios.data_part import DataPart
from parameter_search.estimator_optimizer import EstimatorOptimizer
import matplotlib.pyplot as plt


scen = "base"

a_type = "shift"
scen = Scenario(scen_name=scen,data= "bafu5k.csv", a_type=a_type )

for name,part_scen in scen.part_scenarios.items():
    train_part : DataPart  = part_scen.train
    repair_inputs = train_part.repair_inputs
    oringinal_rmse = train_part.original_scores["full_rmse"]

def min_max(vec):
    min_ = min(vec)
    max_ = max(vec)
    diff = max_ - min_
    return [(v-min_)/diff for v in vec]

for p in [1]:
    imr = IMR_estimator()
    range = imr.suggest_param_range(repair_inputs["injected"])
    param_list = [ {"p":p ,"tau" : tau} for tau in np.linspace(0,0.2,50)]
    res = EstimatorOptimizer(estim=imr,error_score="partial_rmse").param_map(repair_inputs,param_list,run_time=True)
    x,y,t = [],[],[]
    for r in res:
        x.append(r[0]["tau"])
        y.append(r[1])
        t.append(r[2])


    x,y ,t = zip(*sorted(zip(x, min_max(y) , min_max(t))))
    plt.plot(x,y , ls = "--" , marker=".",label= f'p = {p}')
    plt.plot(x,t , ls = "--" , marker=".",label= f'time-{p}')

plt.axhline(y=oringinal_rmse, color='r', linestyle='-' , label = "original_error")
plt.legend()
plt.show()

with open(f'parameterization_{a_type}_partial_imr.txt', 'w') as fp:
    fp.write(f"tau,rmse,time\n")
    for param,score,time  in zip(x,y,t):
        # write each item on a new line
        fp.write(f"{param},{score},{time}\n")




### screen
screen = SCREENEstimator()
range = screen.suggest_param_range(repair_inputs["injected"])
param_list = [ {"smin":-s ,"smax" : s} for s in np.linspace(0,1,40)]
res = EstimatorOptimizer(estim=screen,error_score="partial_rmse").param_map(repair_inputs,param_list,run_time=True)

x, y, t = [], [], []
for r in res:
    x.append(r[0]["smax"])
    y.append(r[1])
    t.append(r[2])

x, y, t = zip(*sorted(zip(x, min_max(y), min_max(t))))
plt.plot(x, y, ls="--", marker=".", label=f's')
plt.plot(x, t, ls="--", marker=".", label=f'time')
plt.show()
with open(f'parameterization_{a_type}_partial_screen.txt', 'w') as fp:
    fp.write(f"s,rmse,time\n")
    for param,score,time  in zip(x,y,t):
        # write each item on a new line
        fp.write(f"{param},{score},{time}\n")
### rpca
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
rpca = Robust_PCA_estimator()
range = rpca.suggest_param_range(repair_inputs["injected"])

for tr in [1.2]:
    param_list = [ {"threshold":tr ,"classification_truncation" : s, "repair_truncation": 4} for s in [1,2,3,4,5,6,7]]
    res = EstimatorOptimizer(estim=rpca,error_score="partial_rmse").param_map(repair_inputs,param_list,run_time=True)

    x, y, t = [], [], []
    for r in res:
        x.append(r[0]["classification_truncation"])
        y.append(r[1])
        t.append(r[2])

    *y , oringinal_rmse = min_max(y+[oringinal_rmse])
    x, y, t = zip(*sorted(zip(x, min_max(y), min_max(t))))
    plt.plot(x, y , marker=".", label=f't = {tr}')
    plt.plot(x, t, ls="--", marker=".", label=f'time-{tr}')

plt.axhline(y=oringinal_rmse, color='r', linestyle='-')
plt.legend()
plt.show()
with open(f'parameterization_{a_type}_partial_rpca.txt', 'w') as fp:
    fp.write(f"k,rmse,time\n")
    for param,score,time  in zip(x,y,t):
        fp.write(f"{param},{score},{time}\n")

# ### cd
from Repair.Dimensionality_Reduction.CD.CDRecEstimator import CDRecEstimator
rpca = CDRecEstimator()
range = rpca.suggest_param_range(repair_inputs["injected"])

for tr in [1.2]:
    param_list = [ {"threshold":tr ,"classification_truncation" : s, "repair_truncation": 4} for s in [1,2,3,4,5,6,7,8]]
    rpca = CDRecEstimator()
    res = EstimatorOptimizer(estim=rpca,error_score="partial_rmse").param_map(repair_inputs,param_list,run_time=True)

    x, y, t = [], [], []
    for r in res:
        x.append(r[0]["classification_truncation"])
        y.append(r[1])
        t.append(r[2])

    *y , oringinal_rmse = min_max(y+[oringinal_rmse])
    x, y, t = zip(*sorted(zip(x, min_max(y), min_max(t))))
    plt.plot(x, y , marker=".", label=f't = {tr}')
    plt.plot(x, t, ls="--", marker=".", label=f'time-{tr}')


plt.axhline(y=oringinal_rmse, color='r', linestyle='-')
plt.legend()
plt.show()


with open(f'parameterization_{a_type}_partial_cd.txt', 'w') as fp:
    fp.write(f"k,rmse,time\n")
    for param,score,time  in zip(x,y,t):
        fp.write(f"{param},{score},{time}\n")