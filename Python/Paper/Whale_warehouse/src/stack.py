class Stack:
    """
    define a stack class to imitate operations in the stack of a warehouse.
    """
    def __init__(self, H, TAU):
        self.items = []
        self.available = int(H*(1-TAU))

    def is_empty(self):
        return self.items == []

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
