import os
from prettytable import PrettyTable
from Repair.res.metrics import RMSE
from Scenarios.BaseScenario import BaseScenario
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

save_folder = "Results"

def error_calculator(scenario_part , col = 0):
    error = RMSE
    repair = scenario_part["repairs"]
    truth = scenario_part["original"]
    injected = scenario_part["injected"]
    print(RMSE(truth.iloc[:,col],injected.iloc[:,col]))
    for key,value in repair.items():
        repair = value["repair"]
        try:
            labels = value["labels"]
        except:
            labels = []
        print(key, error(truth.iloc[:,col],repair.iloc[:,col] , labels=labels))

#save_injection_scenario(data_name, scenario , injected_scenario ,repairs )

def save_injected(injected_scenario,path ,data_name,  file_name = "injected_plots"):
    print("SAVING injected plots")

    x = len([f for f in os.listdir(path) if f[:-5].endswith(file_name) or f[:-4].endswith(file_name)])
    pdf = PdfPages(f'{path}/{file_name}{x or ""}.pdf')
    for k, v in injected_scenario["scenario_data"].items():
        injected = v["injected"]
        injected.plot()
        plt.title(f'{data_name} {k}')
        plt.savefig(pdf, format='pdf')
    pdf.close()


def save_scenario(data_name, scenario , injected_scenario ,repairs , cols ):
    """ name -> generated data_files, plots ,  infos  """

    scenario_name = scenario.scenario_type

    name = data_name
    path = f"{save_folder}/{scenario_name}/{scenario.anomaly_type}/{data_name}"
    try:
        os.makedirs(path)
    except:
        pass

    save_injected(injected_scenario,path,data_name)

    file_name = "repair_plots"
    x = len([ f for f in os.listdir(path) if f[:-5].endswith(file_name) or f[:-4].endswith(file_name)])
    pdf = PdfPages(f'{path}/{file_name}{x or ""}.pdf')

    t = None
    for k, v in injected_scenario["scenario_data"].items():
        alg_repairs = repairs[k]

        if t is None:
            t =  PrettyTable([scenario.small_data_description,"injected"] + list(alg_repairs.keys()))
            t.align = 'l'  # align left
            t.border = False
            t.title = "RMSE"

        truth = v["original"]
        injected = v["injected"]

        table_row = [k]
        table_row.append(sum([RMSE(truth.iloc[:,col],injected.iloc[:,col]) for col in cols]))

        for key , value in alg_repairs.items():

            plt.close()
            repair_df = value["repair"]
            generate_repair_plot(repair_df,truth,injected,cols)
            plt.title(f'{key} {k}')
            plt.savefig(pdf, format='pdf')
            table_row.append(sum([RMSE(truth.iloc[:,col], repair_df.iloc[:,col]) for col in cols]))

        t.add_row(table_row)

    pdf.close()

    with open(path+'/RMSE_table', 'w') as w:
        w.write(str(t))



def generate_repair_plot(repair_df,truth, injected, cols):
    for i,column in enumerate(repair_df.columns):
        alpha = 0.2
        if cols is not None and i not in cols:
            plt.plot(truth[column], alpha=alpha)
            pass
        else:
            plt.plot(truth[column], color="black", )
            plt.plot(injected[column], color="red")
            plt.plot(repair_df[column])


