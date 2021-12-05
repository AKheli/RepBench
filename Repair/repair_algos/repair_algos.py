





def SCREEN_repair(x, indexes=None, t=1, s = 3):
    if indexes is None:
        indexes = np.arange(len(x))

    output =  screen(np.array([indexes, x]).T, datasize=None, T=t, SMIN=-s, SMAX=s)
    output["name"] = f"SCREEN({t},{s})"
    return output

