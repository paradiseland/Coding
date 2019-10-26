class Objective:
    def __init__(self, prefer, obj_coe):
        self.preference = prefer
        self.coefficient = obj_coe

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    # instance a['name']/a['preference']/a['UpperBound'] can get the corresponding value
    def __setitem__(self, key, value):
        self.__dict__[key] = value


if __name__ == '__main__':
    a = Objective('max', [1, 2, 3])
    print(a.preference, a.coefficient)
