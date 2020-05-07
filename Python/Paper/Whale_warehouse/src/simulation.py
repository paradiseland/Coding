# 重点在于 Storage policy and Reshuffling policy 

class Simulation:
    """
    define the overall simulation class to realize discrete event simulation.
    """

    """
    1. arrive at poisson process
    2. system randomly assigns an available robot to order /wait
    3. move in shortest path
    4. robot fetches the retrieval bin.
        dedicated storage: pick up the yop bin
        shared policy: 
                if retrieval bin is on peek: pick up
                else: reshuffling
                        immediate reshuffling 
                        delayed reshuffling
    5. robot transports to designated workstation, drop off and pick up a storage bin
    6. robot transports to storage point. random stack: at any position
                                        zoned stacks: got to the zone determined by turnover
    7. robot drop off the bin
    8.  if previous retrieval includes a reshuffling, then returning blockings to storage rack.
    """

    pass




