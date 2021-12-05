import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-data","-d" ,nargs=1, type=str , default="")
parser.add_argument("-anomaly_type","-at" ,nargs=1, type=str , default="")
parser.add_argument('-algo', nargs=1, default=[])
#parser.add_argument('-algox',nargs=1, default=[])
parser.add_argument('-scenario',nargs=1, default=["simple"])
parser.add_argument('-save',  nargs="*", type=str , default=True )

parser.add_argument('-save',  nargs="*", type=str , default=True )
args = parser.parse_args()
files = args.data[0]