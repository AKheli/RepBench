import os
import csv

from res.plotter import Plotter
from res.metrics import RMSE
import matplotlib as plt

def set_path_to_Repair():
    current_path = __file__
    splitted = current_path.split("Repair")
    os.chdir("".join(splitted[:-1]) + "Repair")


def write_error_file(path, repairs, errors):
    # os.mkdir(path+"/Errors")
    data_sets = set()
    with open(path + "/test", 'w') as f:
        # todo handle unsorted data_sets

        for error in errors:
            f.write(f'rmse ')
            f.write('\n')
            for repair in repairs:
                if repair["data_set"]["name"] not in data_sets:
                    f.write('\n')
                    f.write(repair["data_set"]["name"])
                    f.write('\n')
                    error = RMSE(repair["data_set"]["injected"], repair["data_set"]["truth"], repair.get("labels", []))
                    f.write(f'{str(error)}  {"injected"} ')
                    f.write('\n')
                    data_sets.add(repair["data_set"]["name"])
                error = RMSE(repair["repair"], repair["data_set"]["truth"], repair.get("labels", []))
                f.write(f'{str(error)}  {repair["name"]} ')
                f.write('\n')


class Evaluation_Save:

    def __init__(self, title="test", errors=["rmse"]):
        self.title = title
        self.errors = errors
        self.repairs = []
        self.datasets = []

    # of the top folder e.g scenario name
    def set_title(self, titel):
        self.titel = titel

    def add_error(self, error):
        self.errors.append(error)

    def add_repair(self, repair_output, data_set):
        self.datasets.append(data_set)
        repair_output["data_set"] = data_set
        self.repairs.append(repair_output)

    def save(self):
        path = f'Results/{self.title}'
        try:
            os.mkdir(path)
        except:
            pass
        ##add Errors
        if len(self.errors) > 0 and len(self.repairs) > 0:
            write_error_file(path, self.repairs, self.errors)

        self.save_plot(path)

    def get_repairs_grouped_bad_dataset(self):
        grouped = {}
        for repair in self.repairs:
            name = repair["data_set"]["name"]
            if name not in grouped:
                grouped[name] = [repair]
            else:
                grouped[name] += [repair]
        return grouped

    def save_plot(self, path):
        grouped = self.get_repairs_grouped_bad_dataset()
        for name, repairs in grouped.items():
            first = repairs[0]
            plotter = Plotter(injected=first["data_set"]["injected"], truth=first["data_set"]["truth"], title=name)

            for repair in repairs:
                plotter.add(repair["repair"],repair["name"], repair["name"])
            plot = plotter.get_plot()
            plot.savefig(f"{path}/{name}.pdf")
            plot.close()