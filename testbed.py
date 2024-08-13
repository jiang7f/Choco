class A:
    def __init__(self):
        self.x = 1
    def change(self):
        self.x = 2
    def print(self):
        print(self.x)

a = A()
b = 2
c = (a, b)
c[0].x = 3
c[0].print()