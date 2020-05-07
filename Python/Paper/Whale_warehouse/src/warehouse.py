import numpy
from stack import Stack


class Warehouse:
    """
    Define a Warehouse class to get an available place and to save parameters of warehouse configuration.
    """
    def  __init__(self, width, ):
        self.width = width
        self.length = length
        self.height = height
        self.ratio = self.width / self.length
        self.init()
    

    def init(self):
        record = []
        for i in range(self.width):
            record.append([])
            for j in range(self.length):
                record[i].append(Stack(H,TAU))
        self.record = record
    

    @property
    def capacity(self):
        return self.width * self.length * self.height

    def pick_up(self, place, product):
        self.record[palce[0]][place[1]].push(product)
    
    def drop_off(self, place, product):
        self.record[place[0]][place[1]].push(product)


