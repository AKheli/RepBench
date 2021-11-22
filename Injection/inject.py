import argparse
import json
import os
import pandas as pd
import numpy as np

from res.helper_methods import searchfiles, get_df_from_file
from res.Injector import Anomalygenerator, Multiple_injector

parser = argparse.ArgumentParser()
parser.add_argument("-data","-d" ,nargs=2, type=str ,  required=True)
#parser.add_argument('-sep',nargs=1, default=[','])

parser.add_argument('-save',  nargs="*", type=str , default=False )
parser.add_argument('-plotoff', action='store_false')
parser.add_argument('-withoutlegend', action='store_false')
parser.add_argument('-anomalydetails', action='store_true')

#anomalies
parser.add_argument("-type","-t" ,nargs=1, type=str )
parser.add_argument("-typex" ,"-tx",nargs=2, type=str , help = "types and parameter file")
parser.add_argument("-train_ratio" ,"-tr",nargs=1, default= [0]  , type=float , help = "ratio of the set")

args = parser.parse_args()


filepath = searchfiles(args.data[0] )
dfs = [get_df_from_file(file) for file in filepath]
print(dfs)

savepath = "Data/generated/"

if(args.save or args.save == []):
    if len(dfs) > 1 and len(args.save) > 0 :
        savepath = "Data/generated/"+args.save[0]
        os.mkdir(savepath)

for df, name  in dfs:
    try:
        name = "".join(name.split(".")[:-1])
    except:
        pass

    injected_columns = {} # col -> (series,info)
    for col in args.data[1].split(","):
        print(args.data[1].split(","))
        col = int(col)
        train = int(len(df)*args.train_ratio[0]/100)
        train_set , data = df.iloc[:train,:] , df.iloc[train:,:].copy()

        types = None
        if args.typex is not None:
            injector = Multiple_injector(data,col ,args.typex[1] )
            types = args.typex[0]

        else:
            injector = Multiple_injector(data,col  )
            if args.type is not None:
                types = args.type[0]


        if types is not None:
            for anom in types.split(","):
                anom = anom[0].lower()
                if anom == "a":
                    injector.add_amplitude_shift()
                elif anom == "d":
                    injector.add_distortion()
                elif anom == "g":
                    injector.add_growth()
                elif anom == "e":
                    injector.add_extreme_point()
                else:
                    print(f'anomaly type {anom} not recognized')

        if(args.anomalydetails):
            print()
            for key, value in injector.anomaly_infos.items():
                value = value.copy()
                value["index_range"] = ( value["index_range"][0] , value["index_range"][-1])
                try:
                    value.pop("std_range")
                except:
                    pass
                print(key,value , "\n")

        if(injector is not None):
            injector.repair_print()

        if(args.plotoff):
            injector.plot(legend=args.withoutlegend)

        infos = injector.anomaly_infos
        series = injector.get_injected_series()
        injected_columns[col] = (series,infos)

    if(args.save or args.save == []):
        save_name = name if args.save == [] or len(dfs) > 1 else args.save[0]


        df.to_csv(f"{savepath}/{save_name}_original",  index=False)

        final_dict = {}
        final_dict["train"] = train
        for key,series_info in injected_columns.items():
            df.iloc[train:, key] = series_info[0]
            final_dict[key] = series_info[1]

        df.to_csv(f"{savepath}/{save_name}_injected" ,  index=False)

        with open(f"{savepath}/{save_name}.json", 'w') as fp:
            json.dump(final_dict, fp, indent=1)


