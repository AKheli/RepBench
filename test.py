class A():

    def f(self):
        pass


class A1(A):
    def f(self):
        return 1


class A2():
    def f(self):
        return 2


class B():

    def __init__(self, x):

        if x == 1:
            a = A1()
        if x == 2:
            a = A2()
        
        self.b: A = a
        print(self.b.f())


b = B(1)
b = B(2)
