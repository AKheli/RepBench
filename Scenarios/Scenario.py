import os

import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

import Scenarios.AnomalyConfig as ac
from Repair.algorithms_config import ALGORITHM_COLORS
from Scenarios.scenario_generator import generate_scenario_data
import matplotlib.pyplot as plt

from Scenarios.scenario_saver.plotters import generate_repair_plot, generate_truth_and_injected


class Scenario:
    def __init__(self, scen_name , data , a_type
                 , cols_to_inject=None
                 , train_test_split=0.5):

        assert a_type in ac.ANOMALY_TYPES

        self.a_type = a_type
        self.scen_name  = scen_name
        self.data_name = data.split(".")[0]
        self.part_scenarios = generate_scenario_data(scen_name,data,a_type,cols_to_inject,train_test_split,)

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
            try:
                os.mkdir(algo_path)
            except:
                pass
            plt.close('all')
            for i,(part_scen_name,scenario_part)  in enumerate(self.part_scenarios.items()):
                truth , injected = scenario_part.truth , scenario_part.injected
                cols = scenario_part.injected_columns
                klass = scenario_part.class_
                axis = plt.gca()
                axis.set_rasterization_zorder(0)
                axis.set_title(part_scen_name)
                algo_part = scenario_part.repairs[repair_name]

                repair_df = algo_part["repair"]
                axis.set_xlim(truth.index[0] - 0.1, truth.index[-1] + 0.1)

                line, = plt.plot(truth.iloc[:, cols[0]])
                lw = plt.getp(line, 'linewidth')
                axis.set_prop_cycle(None)
                generate_repair_plot(repair_df, cols, repair_name, lw, axis)
                generate_truth_and_injected(truth, injected, cols, klass, lw, axis , alpha = 0.5)
                axis.xaxis.set_major_locator(MaxNLocator(integer=True))
                plt.savefig(f"{algo_path}/{part_scen_name}.svg")
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

            try:
                os.makedirs(error_path)
            except:
                pass


            # for name_type in metric_df.columns:
            #     new_df = pd.DataFrame(metric_df[name_type].to_list(), columns=[metric])
            #
            #     new_df.to_csv(f'{error_path}/{col}.txt')



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

