class Money:
    def __init__(self):
        self.__money = 0

    # 使用装饰器对money进行装饰，那么会自动会添加一个叫money的属性，当调用获取money的值时，调用装饰的方法
    @property
    def money(self):
        return self.__money

    # 使用装饰器对money进行装饰，当对money设置值时，调用装饰的方法
    @money.setter
    def money(self, value):
        if isinstance(value, int):
            self.__money = value
        else:
            print("error:不是整型数字")


a = Money()
a.money = 100
print(a.money)
a.money = 1000
print(a.money)