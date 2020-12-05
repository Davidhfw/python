class Generic:
    """fttet"""
    # def __init__(self):
    #     self.value = None
    def test(self):
        print("beijing")


g = Generic()
g.__setattr__("value", 1)
print(g.__getattribute__("value"))
print(g.__doc__)
print(g.__module__)
print(g.__dict__)
