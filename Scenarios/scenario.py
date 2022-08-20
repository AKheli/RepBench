import os
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator
import Scenarios.AnomalyConfig as ac
from repair.algorithms_config import ALGORITHM_COLORS
import matplotlib.pyplot as plt

class Scenario:
    def __init__(self, scen_name , data , a_type):
        assert a_type in ac.ANOMALY_TYPES
        self.a_type = a_type
        self.scen_name  = scen_name
        self.data_name = data.split(".")[0]
        self.part_scenarios = {}

    def add_part_scenario(self,data_part, part_key):
        self.part_scenarios[part_key] = data_part

    @property
    def name_train_test_iter(self):
        return iter( [ (name , scen_part.train , scen_part ) for name, scen_part in self.part_scenarios.items()])

    def get_amount_of_part_scenarios(self):
        return len(self.part_scenarios)


    @property
    def repair_names(self):
        return set(sum([p.repair_names for k,p in self.part_scenarios.items()],[]))

    def save_repair_plots(self,path):
        for repair_name in self.repair_names:
            algo_path = f'{path}/{repair_name}'

            Path(algo_path).mkdir(parents=True, exist_ok=True)

            plt.close('all')
            for i,(part_scen_name,scenario_part)  in enumerate(self.part_scenarios.items()):
                full_truth , full_injected = scenario_part.truth , scenario_part.injected
                cols = scenario_part.injected_columns
                klass = scenario_part.class_
                axis = plt.gca()
                axis.set_rasterization_zorder(0)
                axis.set_title(f'{part_scen_name}')
                algo_part = scenario_part.repairs[repair_name]
                full_repair = algo_part["repair"]

                for col in cols:
                    col_nbr = col+1
                    a_ranges = scenario_part.get_anomaly_ranges(klass.iloc[:,col])
                    n_ranges = min(len(a_ranges),3)
                    selected_ranges_i = np.random.choice(range(len(a_ranges)),size=n_ranges,replace=False)
                    for a_index , range_index in enumerate(selected_ranges_i):
                        range_ = a_ranges[range_index]
                        start, end = max(0,min(range_)-20) , min(full_truth.shape[0],max(range_)+20)
                        truth = full_truth.iloc[start:end,col]
                        truth , index = truth.values , truth.index.values
                        injected = full_injected.iloc[start:end,col].values
                        repair = full_repair.iloc[start:end,col].values
                        axis.set_xlim(index[0] - 0.1, index[-1] + 0.1)
                        line, = plt.plot(index,truth)
                        lw = plt.getp(line, 'linewidth')

                        axis.set_prop_cycle(None)
                        ### repair plot

                        ###
                        mask = (injected !=truth).astype(int)
                        mask[1:] += mask[:-1]
                        mask[:-1] += mask[1:]
                        mask = np.invert(mask.astype(bool))
                        masked_injected =  np.ma.masked_where(mask, injected)
                        plt.plot(index,masked_injected, color="red", ls='--', marker="." ,label="injected")
                        plt.plot(index,repair, lw=lw/2 , label= "repair" , color="blue")

                        plt.plot(index,truth, color="black", lw=lw, label="truth")
                        plt.legend()
                        axis.xaxis.set_major_locator(MaxNLocator(integer=True))
                        plt.savefig(f"{algo_path}/{self.scen_name}_{part_scen_name}_TS{col_nbr}_{a_index}.svg")
                        plt.close('all')


    def score_dfs(self):
        used_scores = []
        full_dict = {}
        for part_name, part in self.part_scenarios.items():
            full_dict[part_name] = {}
            for (alg_name, alg_type) , scores in part.repair_metrics.items():
                full_dict[part_name][(alg_name,alg_type)] = scores
                used_scores += list(scores.keys())

        full_df = pd.DataFrame.from_dict(full_dict,orient="index")
        full_df.index.name = self.scen_name
        retval = {score : full_df.applymap(lambda x: x.get(score,np.NAN)) for score in set(scores)}
        return retval

    def save_error(self,path):
        from itertools import cycle

        initial_path = path
        lines = ["solid", "dashed", "dotted", "dashdot"]
        # colors = ["red", "green", "green",  "green", "purple", "blue"]
        path = f"{path}/error"
        try:
            os.makedirs(path)
        except:
            pass

        plt.clf()
        plt.close()

        for metric , metric_df in self.score_dfs().items():
            error_path = f'{path}/{metric}'
            if "time" in metric:
                error_path = f'{"/".join(initial_path.split("/")[:-2])}/runtime'
                #print(metric_df)

            try:
                os.makedirs(error_path)
            except:
                pass

            columns = list(metric_df.columns)
            cyclers = {}
            for name_type in columns:
                color = ALGORITHM_COLORS[name_type[1]]
                if color not in cyclers:
                    cyclers[color] = cycle(lines)
                plt.plot(metric_df[name_type], marker='x', label=name_type[0], color=color, ls=next(cyclers[color]))
            plt.xlabel(metric_df.index.name)
            plt.ylabel(metric)
            lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.savefig(f'{error_path}/{metric}.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
            plt.clf()
            plt.close()
            metric_df.columns = [name for name,type in metric_df.columns]
            metric_df.to_csv(f'{error_path}/{metric}.txt')

