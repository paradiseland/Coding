class Workstation:
    """
    define a workstation class to describe available workstation and its state.
    """

    def __init__(self, num_of_workstations):

        self.num = num_of_workstations
        self.dis = L/(self.num/2+1)

