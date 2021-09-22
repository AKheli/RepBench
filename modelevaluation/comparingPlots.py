import matplotlib.pyplot as plt


def visualize(data, repair, truth=None, time=None, section=None, repair_color="blue", data_color="black",
              truth_color="green" , title = "title"):
    if section is not None:
        if isinstance(section, tuple):
            l, u = section
            data = data[l:u]
            repair = repair[l:u]
            if truth is not None:
                truth = truth[l:u]
            if time is not None:
                time = time[l:u]
        else:
            print("sections has to be a tuple")
    if time is None:
        time = range(len(data))
    plt.plot(time,data , color = data_color)
    plt.plot(time,repair,color = repair_color)
    if truth is not None:
        plt.plot(time,truth, color = truth_color)


    plt.gca().set(title=title, xlabel="time", ylabel="Value")

    plt.show()

