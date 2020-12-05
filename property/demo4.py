class Goods:
    def __init__(self):
        self.age = 18

    @property
    def price(self):
        return self.age

    # 方法名.setter
    @price.setter
    def price(self, value):
        self.age = value

    @price.deleter
    def price(self):
        del self.age


obj = Goods() # 实例化对象
print(obj.age) # 直接获取age属性值
obj.age = 123   # 修改age值
del obj.age   # 删除age属性的值