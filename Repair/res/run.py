from Repair.evaluation_saver import Evaluation_Save
from Repair.extract_values import get_data
from Repair.repair_algos.repair_algos import IMR_repair, SCREEN_repair

datafiles = ["test/BAFU","test/YAHOO","test/Humidity"]
col = 0
saver = Evaluation_Save()


for file in datafiles:
    data = get_data(file)
    x = data["injected"].iloc[:, col]
    truth = data["original"].iloc[:, col]
    anom_info = data["info"][str(col)]

    data_info = {"name" : file.split("/")[-1] , "truth" : truth , "injected" : x}
    imr = IMR_repair(x, truth,p=1)
    saver.add_repair(imr, data_info )
    imr = IMR_repair(x, truth, p = 2)
    saver.add_repair(imr, data_info)
    imr = IMR_repair(x, truth, p = 3)
    saver.add_repair(imr, data_info)
    screen = SCREEN_repair(x, s=0.1)
    saver.add_repair(screen,data_info)
    screen = SCREEN_repair(x, s=1)
    saver.add_repair(screen, data_info)
    screen = SCREEN_repair(x, s=3)
    saver.add_repair(screen, data_info)

saver.save()
