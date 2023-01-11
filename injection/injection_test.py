
import inject

print("Hallo")

import os
curr_wd = os.getcwd()
root_dir = "RepairBenchmark"
os.chdir("".join(curr_wd.split(root_dir)[:-1]) + root_dir)

input = "-a shift -f 1 -r 1 -ts 1,2 -d elec"
inject.main(input)
