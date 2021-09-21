import numpy as np

import timeit
i = 0

#RMS = lambda x, y: np.mean(np.square(x - y)) ** (1 / 2)


def local(sub_times, sub_values, pre_time , pre_val , kp_time , kp_val , SMIN = -6, SMAX = 6):
    global i
    i = i+1
    #print(sub_times)
    d_time = kp_time - sub_times
    xklist =  [kp_val] + list(sub_values + SMIN * d_time)[1:] + list( sub_values + SMAX * d_time)[1:]
    xklist = sorted(xklist)
    xMid = xklist[len(sub_values)-1]
    lowerBound = pre_val + SMIN*(kp_time - pre_time)
    upperBound = pre_val + SMAX*(kp_time - pre_time)
    if upperBound < xMid:
        return upperBound
    if lowerBound > xMid:
        return lowerBound
    return xMid


# Press the green button in the gutter to run the script.
datafile = "stock10k.datasets"

if __name__ == '__main__':
    print("start")


def screen(  Series , datasize = None  ,T = 1  ):
    #Series = (pandas.read_csv(datafile , names = ("timestamp", "mod" , "true"))).to_numpy()

    #maybe throw an error message here if datasize is to big

    if datasize == None:
        timestamps = Series[:, 0]
        mod = Series[:, 1]
        truth =  Series[:, 2]
    else:
        timestamps = Series[:datasize ,0]
        mod = Series[:datasize,1]
        truth =  Series[:datasize, 2]

    mod = mod*1
    truth = truth*1


    #RMS = lambda x,y: np.mean(np.square(x-y))**(1/2)

    modcopy = mod + 0



    preEnd = -1
    wStartTime =  timestamps[0]
    wEndTime = wStartTime
    wGoalTime = wStartTime + T

    tmp_indices = [0] #tmp series
    prepoint_index = 0

    for index , cur_time in enumerate(timestamps[1:],1):
        if(cur_time > wGoalTime):
            while True:
                if(len(tmp_indices) == 0):
                    tmp_indices.append(index)
                    wGoalTime = cur_time + T
                    wEndTime = cur_time
                    break

                kp_index = tmp_indices[0]
                wStartTime = timestamps[kp_index]
                wGoalTime = wStartTime + T

                if cur_time <= wGoalTime:
                    tmp_indices.append(index)
                    wEndTime = cur_time
                    break

                curEnd = wEndTime


                if preEnd == -1:
                    prepoint_index = kp_index

                mod[kp_index] = local(timestamps[tmp_indices], mod[tmp_indices]
                                      ,timestamps[prepoint_index] , mod[prepoint_index]
                                      , timestamps[kp_index] , mod[kp_index])

                prepoint_index = kp_index
                preEnd = curEnd
                tmp_indices.pop(0)
        else:
            if cur_time > wEndTime:
                tmp_indices.append(index)
                wEndTime = cur_time

    #print(RMS(mod,truth))

    return mod



