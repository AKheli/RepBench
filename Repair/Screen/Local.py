import numpy as np

i = 0

#RMS = lambda x, y: np.mean(np.square(x - y)) ** (1 / 2)


def local(sub_times, sub_values, pre_time , pre_val , kp_time , kp_val , SMIN = -3, SMAX = 3):
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


def screen(  Series , datasize = None  ,T = 1   , SMIN = -3, SMAX = 3):
    #Series = (pandas.read_csv(datafile , names = ("timestamp", "mod" , "true"))).to_numpy()

    if Series.ndim == 1:
        original = Series
        timestamps = np.arange((len(original)))
    else:
        if datasize == None:
            timestamps = Series[:, 0]
            original = Series[:, 1]
            #truth =  Series[:, 2]
        else:
            timestamps = Series[:datasize ,0]
            original = Series[:datasize,1]
            #truth =  Series[:datasize, 2]

    mod = original.copy()

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
                                      , timestamps[kp_index] , mod[kp_index] ,  SMIN = SMIN, SMAX = SMAX)

                prepoint_index = kp_index
                preEnd = curEnd
                tmp_indices.pop(0)
        else:
            if cur_time > wEndTime:
                tmp_indices.append(index)
                wEndTime = cur_time

    #print(RMS(mod,truth))
    print(sum(abs(mod-original)))
    return {"repair" : mod , "smin" : SMIN ,"smax": SMAX , "T": T}

5
values = np.array([12, 12.5, 13, 10, 15, 15.5])
# print(sum(abs(values-mod1)))
modified = screen(values , T=5 , SMIN=-0.5, SMAX= 0.5)

# modified_global = LPconstrainedAE(values.copy(), min=2, max= 2)
#
# print("local",np.mean(abs(values-modified))**(1/2))
# print("global",np.mean(abs(values-modified_global))**(1/2))
#
#
# plt.plot(range(len(timestamps)),values, 'b' , label = "original")
# plt.plot(range(len(timestamps)),modified, 'o' , label = "local")
# plt.plot(range(len(timestamps)),modified_global, 'x' , label = "local" , color = "red")
#
#
# plt.show()
#
#
# timestamps =  np.array([1,2,3,4,5,6,8,9,10, 11 ,12,13,15, 16 ,17 ],dtype=int)
# values = np.array([5,6,5,6,7,6,5,5,5,16.5,18,17.5,20,8,6])
#
#
# min = 2
# max = 2
# modified = screen(np.array([timestamps,values]).T , T=1 , SMIN=-min, SMAX= max)
# modified_global = LPconstrainedAE(values.copy(), min=min, max= max)
#
# print("local",np.mean(abs(values-modified))**(1/2))
# print("global",np.mean(abs(values-modified_global))**(1/2))
#
#
# plt.plot(timestamps,values, 'b' , label = "original")
# plt.plot(timestamps,modified, 'o' , label = "local")
# plt.plot(timestamps,modified_global, 'x' , label = "local" , color = "red")
#
# plt.show()