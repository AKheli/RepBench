import os
from Scenarios.metrics import RMSE
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import pandas as pd

from Scenarios.scenario_helpers.error_calulation import generate_error_df
from Scenarios.scenario_helpers.error_table import RepairEvaluator
from Scenarios.scenario_helpers.plotters import  scenario_plot

save_folder = "Results"

#save_injection_scenario(data_name, scenario , injected_scenario ,repairs )

def save_injected(injected_scenario,path ,data_name,  file_name = "injected_plots"):
    print("SAVING injected plots")

    x = len([f for f in os.listdir(path) if f[:-5].endswith(file_name) or f[:-4].endswith(file_name)])
    #pdf = PdfPages(f'{path}/{file_name}{x or ""}.pdf')
    for k, v in injected_scenario["scenario_data"].items():
        injected = v["injected"]
        injected.plot()
        plt.title(f'{data_name} {k}')
        #plt.savefig(pdf, format='pdf')
    #pdf.close()

def save_scenario(repaired_scenario_dict):
    scenario_type = repaired_scenario_dict["scenario_type"]
    scenario_name = scenario_type.scenario_type
    data_name = repaired_scenario_dict["data_name"]

    path = f"{save_folder}/{scenario_name}/{scenario_type.anomaly_type}/{data_name}"
    try:
        os.makedirs(path)
    except:
        pass


    filename = "repair_plots"

    scenario_data = repaired_scenario_dict["scenario_data"]
    error_df = generate_error_df(scenario_data, RMSE)
    error_df.index.name = scenario_type.small_data_description
    error_df.plot()
    plt.show()

    scenario_plot(scenario_data,path)








