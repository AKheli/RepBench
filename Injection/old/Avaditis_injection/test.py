from distortion_injector import DistortionInjector
import pandas as pd
import numpy as np

datafile = "export.json"
#Series = pd.Series(pd.read_json(datafile))
Series = pd.read_json(datafile)
print(Series['dataset_series_json'])

injected =  DistortionInjector(Series)