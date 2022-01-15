from matplotlib import pyplot as plt



import time


class B:
    def predict(self):
        t = time.time()
        results = self._predict()
        print("time" ,time.time()-t)
        return results


class A(B):
    def _predict(self):
        return [a**3.5 for a in range(100000)]



