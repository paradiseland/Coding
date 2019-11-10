"""
define the result
"""


class Result:
    """
    define the output result class
    """

    def __init__(self, is_solved, objective_value, x_value, status):
        self.is_solved = is_solved
        self.obj_value = objective_value
        self.x_value = x_value
        self.status = status

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    # instance c['name']/c['coefficients']/c['right'] can get the corresponding value
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def print_result(self):
        print(self.is_solved)
        print(self.obj_value)
        print(self.x_value)


if __name__ == '__main__':
    BOOLEAN = True
    OBJ = 20
    X = [2, 3, 4]
    ST = '101'
    RES = Result(BOOLEAN, OBJ, X, ST)
    print('Result:\n', RES['isSolved'], RES['objValue'], RES['xValue'])
