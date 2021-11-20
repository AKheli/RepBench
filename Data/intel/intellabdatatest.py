from Repair.repair_algos.IMR import IMR as IMR

data = pd.read_csv("ild3k.Data", names = ["index", "x", "y_0", "truth" , "label"], header = None)
print(data)

x = np.array(data["x"])
truth = np.array(data["truth"])
labels = np.arange(len(x))[data["label"]]
y_0 = np.array(data["y_0"])

result = imr2(x,y_0,labels,tau=0.2,p=3)
IMR.plot(x, result, truth, labels = labels)

java_result = np.array(pd.read_csv("myfile.csv", header = None))[:, 0]

print( sum(result-java_result))

def rms(x,y,labels= []):
    labeled_x , labeled_y = x[labels] , y[labels]
    return np.sqrt(
        (np.sum(np.square(x-y))- np.sum(np.square(labeled_x - labeled_y)))
        /(len(x)-len(labeled_x))
        )

print("original rms" , rms(y_0,truth, labels))
print("rms java" , rms(java_result,truth, labels))
print("rms" , rms(result,truth, labels))


result = imr2(x,y_0,labels,tau=0.1,p=3)
print("rms" , rms(result,truth, labels))

result = imr2(x,y_0,labels,tau=0.1,p=1)
print("rms" , rms(result,truth, labels))

labels = np.arange(500)[data["label"][1500:2000]]
IMR.plot(x[1500:2000], result[1500:2000], truth[1500:2000], labels = labels, index= np.arange(1500, 2000))

