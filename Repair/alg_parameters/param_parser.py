import os
A = "a"
def set_path_to_Repair():
    current_path = __file__
    splitted = current_path.split("Repair")
    os.chdir("".join(splitted[:-1]) + "Repair")

def cast(value):
    try:
        return int(value)
    except:
        try:
            return float(value)
        except:
            return value


def parse_params(   filename = "default_params"   , algx = False):
    set_path_to_Repair()
    with open(f"alg_parameters/{filename}") as f:
        lines = f.readlines()
    algs = []
    currentkeys = []
    current_alg = None

    for line in lines:
        line = line.strip()
        if len(line) > 0:
            if line[0] == "#":
                continue
            line = line.split()
            if line[0] == "!":
                current_alg = line[1]
                currentkeys = line[2:]

            else:
                algs.append( { "name" :current_alg , "params" :{ k: cast(v) for k,v in zip(currentkeys,line)}  }      )

    return algs








