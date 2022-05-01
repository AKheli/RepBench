import numpy as np
import pandas as pd
import os
def create_summary(error = "RMSE"):
    counter = {}
    for path in [x[0] for x in os.walk("Results") if x[0].endswith(error)]:
        results , scen , a_type , data_set , *_  = path.split("/")

        file_name = error+".txt"
        df = pd.read_csv(f'{path}/{file_name}',sep="," , index_col=0)
        mean_dict = {column : np.average(df[column],weights=np.arange(1,len(df[column])+1)) for column  in df }
        sorted_by_mean = [y for y, _ in sorted(mean_dict.items(),key = lambda x : x[1]) ]
        for i,alg in enumerate(sorted_by_mean):
            counting_list = counter.get(alg,[0, 0, 0, 0, 0])
            counting_list[i] = counting_list[i] + 1
            counter[alg] = counting_list
    print(counter)
    print(*sorted(counter.items() , key = lambda x : sum( i*v for i,v in enumerate(x[1]))), sep="\n")
if __name__ == '__main__':
    create_summary()

