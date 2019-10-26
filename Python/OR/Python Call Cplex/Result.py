class Result:

    def __init__(self, is_solved, objective_value, x_value,status):
        self.isSolved = is_solved
        self.objValue = objective_value
        self.xValue = x_value
        self.status = status

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    # instance c['name']/c['coefficients']/c['right'] can get the corresponding value
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def print_result(self):
        print(self.isSolved)
        print(self.objValue)
        print(self.xValue)


if __name__ == '__main__':
    boolean = True
    obj = 20
    x = [2, 3, 4]
    res = Result(boolean, obj, x)
    print('Result:\n', res['isSolved'], res['objValue'], res['xValue'])
