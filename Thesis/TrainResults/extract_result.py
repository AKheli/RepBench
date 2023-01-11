folder = "imr"

file_name = "train_results.toml"
import toml


scen = "a_size"
dict = toml.load(f"{folder}/{file_name}")

data = ["msd" ,"bafu", "humidity" , "elec"]
errors = ["full_rmse", "partial_rmse", "mae"]
a_type = ["outlier", "shift", "distortion"]

f_screen = lambda d : f'& {round(d["smin"],2)}  & {round(d["smax"],2)}'
f_rpca = lambda d : f'& {int(d["p"])}  & {round(d["tau"],3)}'
f_imr =  lambda d : f'& {int(d["p"])}  & {round(d["tau"],3)}'
f = f_imr
name_map = {"distortion" : "var change"
    , "shift" : "shift"
    , "outlier" : "outlier"}

for d in data:
    print(d)
    for a in a_type:
        print("&" , name_map[a])
        for error in errors:
            for k , v in dict.items():
                name =  "".join(v["names"])
                if scen in name and  d in name and a in name and error in name:
                    print(f(v))
        print("\\\\")