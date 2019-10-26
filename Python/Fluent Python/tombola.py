import abc


class Tombola(abc.ABC):
    pass

    @classmethod
    def load(cls, iterable):
        pass
        # 从可迭代对象中添加元素

    @classmethod
    def pick(cls):
        pass
        # 随机删除元素，并将其返回

    def loaded(self):
        pass
        # 至少一个元素则返回True
        return bool(self.inspect())

    def inspect(self):
        pass
        # 返回现有元素构成的有序元组
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))

a = Tombola()


from os import walk

import itertools


