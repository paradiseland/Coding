"""
define the class of constraints in the programming.
"""


class Constraint:

    def __init__(self, name, constraint_coefficients, relation, right_side,):
        self.coefficients = constraint_coefficients
        self.relation = relation
        self.right = right_side
        self.name = name

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    # instance c['name']/c['coefficients']/c['right'] can get the corresponding value
    def __setitem__(self, key, value):
        self.__dict__[key] = value


if __name__ == '__main__':
    coe = [1, 2, 3]
    EQ = 'equal'
    LE = 'less'
    GE = 'greater'
    c1 = Constraint('C1', coe, EQ, 3)
    print(c1['name'], c1['coefficients'], c1['relation'], c1['right'])
    constraints = []
    sense = [EQ, LE, LE]
    coe1 = [[1, 2, 3],
            [2, 3, 5],
            [3, 4, 5]]
    for i in range(3):
        # 'y%d' % i 产出名称序列
        constraints.append(Constraint('c%d' % i+1, coe[i], sense[i], 3))
