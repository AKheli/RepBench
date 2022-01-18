from play2 import B ,time_it


class A(B):
    @time_it
    def predict(self):
        x =  [a**3.5 for a in range(10000000)]
        return None


