import sys

import numpy as np
import pandas as pd

from Injector import Anomalygenerator

if __name__ == "__main__":
    print("Enter data file path")
    print("example Data/SAG.csv")

    while(True):
        try:
            path = input()
            print(path)
            if path[-3:] == "csv":
                df = pd.read_csv(path, sep=';', header=0)

            break
        except FileNotFoundError:
            print("no such file found , try agian")

    print(df)
    print("select ts name")
    while(True):


            ts_name = input()
            ts = df[df["ts_name"] == ts_name]

            if len(ts) > 1:
                print(ts)
                break
            else:
                print("ts not found")


    print("select value vectore")
    while (True):
        try:
            value = input()
            values = np.array(ts[value])
            break
        except KeyError:
            print("no such line in the data frame, try agian")

    print(values)

    injector = Anomalygenerator(values)
    while (True):
        print("select anomaly to inject: amplitude_shift , growth_change , distortion")
        anomaly = input()

        print("give a mount of anomalies")
        amount  = int(input())
        x = anomaly[0]


        if x == "a":
            injector.add_amplitude_shift(number_of_ranges=amount)
        if x ==  "g":
            injector.add_growth(number_of_ranges=amount)

        #case ds
        injector.plot()
        ts = ts.copy()
        ts["injected_series"] = injector.get_injected_series().copy()
        print(ts)
        ts.to_csv("injected")
        break


