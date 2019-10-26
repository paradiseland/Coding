class Variable:

    def __init__(self, type_of_num, bound, name):
        self.type = type_of_num
        self.LowerBound = bound[0]
        self.UpperBound = bound[1]
        self.name = name

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    # instance a['name']/a['LowerBound']/a['UpperBound'] can get the corresponding value
    def __setitem__(self, key, value):
        self.__dict__[key] = value


if __name__ == '__main__':
    variableList = []
    for i in range(3):
        # 'y%d' % i 产出名称序列
        variableList.append(Variable('ICI'[i], [i, float('inf')], 'x%d' % i+1))
    a = Variable("int", [0, float('inf')], 'a')
    print(a.type)

