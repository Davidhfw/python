
"""
Python底层语言设计层面如何实现metaclass
第一，所有的Python用户定义类，都是type这个类的实例
第二，用户自定义类，只不过是type类的__call__运算符重载
第三，metaclass是type的子类，通过替换type的__call__运算符重载机制，“超越变形”正常的类
"""

import yaml

class Monster(yaml.YAMLObject):
    yaml_tag = u'!Monster'

    def __init__(self, name, hp, ac, attacks):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks

    def __repr__(self):
        return "%s(name=%r, hp=%r, ac=%r, attacks=%r)" % ( self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)


yaml.load_all("""
    --- !Monster
    name: Cave spider
    hp: [2,6] # 2d6
    ac: 16
    attacks: [BITE, HURT]
""")
Monster(name='Cave spider', hp=[2, 6], ac=16, attacks=['BITE', 'HURT'])
print(yaml.dump(Monster(name='Cave lizard', hp=[3, 6], ac=16, attacks=['BITE', 'HURT'])))

class MyClass:
    pass

instance = MyClass()
print(type(instance))
print(type(MyClass))

class MyClass1:
    data = 1

instance = MyClass1()
print(MyClass1)
print(instance)
print(instance.data)

MyClass1 = type('MyClass1', (), {'data': 1})
instance = MyClass1()
print(MyClass1)
print(instance)
print(instance.data)


