import os

from Scenarios.BaseScenario import BaseScenario
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

save_folder = "Results"


def save_injection_scenario(scen: BaseScenario, injected_data, original,info="text"):
    """ name -> generated data_files, plots ,  infos  """

    scenario_name = scen.scenario_type

    for name , data_dict in injected_data.items():
        name = name.split(".")[0]
        path = f"{save_folder}/{scenario_name}/{scen.anomaly_type}/{name}"
        try:
            os.makedirs(path)
        except:
            pass

        print("SAVING")

        x = None
        file_name = "injected_plots"
        x = len([ f for f in os.listdir(path) if f[:-5].endswith(file_name) or f[:-4].endswith(file_name)])

        pdf = PdfPages(f'{path}/{file_name}{x or""}.pdf')
        print(injected_data)
        for d in data_dict["injected_data"]:
            try:
                d = d.drop("class",axis = 1)
            except:
                pass
            d.plot()
            plt.title(name)
            plt.savefig(pdf, format='pdf')
        pdf.close()

        #save_plot(path, plt, f'{name}_original')


def save_plot(path, plt, name):
    plt.savefig(f"{path}/{name}.pdf", bbox_inches='tight')
