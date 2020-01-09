"""Capacited Vehicles Routing Problem (CVRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from get_parameter import get_parameters
from haversine import get_distance
from plot2 import plot2

def create_data_model(infomation, dist, trunk):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = dist
    data['demands'] = infomation["demand_weight"]
    data['vehicle_capacities'] = [trunk[0]]*80
    data['num_vehicles'] = 80
    data['depot'] = 0
    return data


def add_capacity_constraints(routing, data, demand_callback):
    """Adds capacity constraint"""
    capacity = "Capacity"
    routing.AddDimensionWithVehicleCapacity(
        demand_callback,
        0, # null capacity slack
        data["vehicle_capacities"], # vehicle maximum capacities
        True, # start cumul to zero
        capacity)



def print_solution(data, manager, routing, assignment, loc):
    """Prints assignment on console."""
    total_distance = 0
    total_load = 0
    Tour = []
    Load = []
    for vehicle_id in range(data['num_vehicles']):
        Tour.append([])
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            Tour[vehicle_id].append(node_index)
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        Tour[vehicle_id].append(0)
        Load.append(route_load)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}km\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
        
    print('Total distance of all routes: {}km'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))
    print(Tour)
    plot2(Tour,location=loc, load=Load)


def main(porb):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    file_name = "assignment.xls"
    info, trunks = get_parameters(file_name)
    trunk = trunks[0]
    infomation = info[prob]
    loc = infomation["location"]
    dist = get_distance(infomation["location"])
    data = create_data_model(infomation, dist, trunk)


    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(data, manager, routing, assignment, loc)


if __name__ == '__main__':
    prob = 2
    main(prob)




