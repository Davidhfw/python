class Goods(object):
    def __init__(self):
        self.p = 100
        self.d = 0.8

    def get_price(self):
        return self.p * self.d

    def set_price(self, value):
        self.p = value

    def del_price(self):
        del self.p

    x = property(get_price, set_price, del_price, "I'm the 'x' property.")


c = Goods()
print(c.x)
c.x = 299
print(c.x)
del c.x
