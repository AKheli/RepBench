import argparse
import numpy as np


from alg_parameters.param_parser import parse_params
from evaluation_saver import Evaluation_Save
from extract_values import get_data
from repair_algos.repair_algos import IMR_repair, SCREEN_repair

parser = argparse.ArgumentParser()
parser.add_argument("-data","-d" , type=str , default="" , required=True)
parser.add_argument("-col","-c" ,nargs=1, type=str , default="0")

parser.add_argument('-algo',   type = str,  default="")
parser.add_argument('-algox', type = str )


parser.add_argument('-save',  nargs="*", type=str , default=True )
parser.add_argument('-plotoff', action='store_false')
parser.add_argument('-withoutlegend', action='store_false')

args = parser.parse_args()

files = args.data

datafiles = files.split(",")


saver = Evaluation_Save()

for file in datafiles:
    col = str(args.col)
    data = get_data(file)
    anom_info = data["info"][str(col)]
    train = anom_info.get("train", 0 )
    x = data["injected"].iloc[train:, int(col)]
    truth = data["original"].iloc[train:, int(col)]

    data_info = {"name" : file.split("/")[-1] , "truth" : truth , "injected" : x}

    if args.algo != "":
        params = parse_params()
        algos = args.algo.lower().split(",")

        algo_dict = {d["name"]: d["params"] for d in params}

        for i in algos:
            if i == "imr":
                result =   IMR_repair(x,truth,**algo_dict["imr"])
                saver.add_repair(result, data_info)
            if i == "screen":
                result =   SCREEN_repair(x,**algo_dict["screen"])
                saver.add_repair(result, data_info)

    if args.algox is not None:
        algos = parse_params(args.algox)

        for a in algos:
            if a["name"] == "imr":
                result = IMR_repair(x, truth, **a["params"])
                saver.add_repair(result, data_info)
            if a["name"] == "screen":
                result = SCREEN_repair(x, **a["params"])
                saver.add_repair(result, data_info)


saver.save()


    #
