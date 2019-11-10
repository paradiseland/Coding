"""
define the variable feature of the problem 
"""


class Variable:
    """
    define the variable
    """

    def __init__(self, type_of_num, bound, name):
        self.type = type_of_num
        self.lower_bound = bound[0]
        self.upper_bound = bound[1]
        self.name = name

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    # instance a['name']/a['LowerBound']/a['UpperBound'] can get the corresponding value
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __setattr__(self, name, value):
        return super().__setattr__(name, value)


if __name__ == '__main__':
    VARIABLE_LIST = []
    for i in range(3):
        # 'y%d' % i 产出名称序列
        VARIABLE_LIST.append(
            Variable('ICI'[i], [i, float('inf')], 'x%d' % (i+1)))
    print(VARIABLE_LIST[0].name, VARIABLE_LIST[0].lower_bound,
          VARIABLE_LIST[0].upper_bound)
