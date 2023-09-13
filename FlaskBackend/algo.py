 
# [START import]
from functools import partial
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import pandas as pd
import copy
import warnings
warnings.filterwarnings("ignore")
# [END import]

tot = 0
num_locations = 0
num_vehicles = 0
dist_mat = []
time_mat = []
max_time = 300
time_window = [(0, 0)]
total_capacity = 500000
demands = [0]
demand_copy = []
vehicle_routes = []
matr = []
new_matr = []
new_distance_after_pickup = []
new_distance_before_pickup = []
time_route = []
vehicle_time_limit = []
horizon = 300
weight_at_each_point = []
Extra_weight = []
indexpoint_weight_at_each_point = []
total_dynamic_points = 0
penalties = []
base = 0
dynamic_latitudes = []
dynamic_longitudes = []


# [START data_model]
def create_data_model_cvrptw(num_locations, time_window, demands, num_vehicles, total_capacity):
    """Stores the data for the problem."""
    data = {}

    data['num_locations'] = num_locations
    data['time_windows'] = time_window

    data['demands'] = demands

    # update penalties array
    for i in range(1,num_locations):
        penalties[i] = penalties[i] + demands[i]
    
    data['time_per_demand_unit'] = 5  # 5 minutes/unit
    data['num_vehicles'] = num_vehicles
    data['vehicle_capacity'] = total_capacity
    data['depot'] = 0
    return data
    # [END data_model]



#######################
# Problem Constraints #
#######################

def create_distance_evaluator_cvrptw(data, dist_mat):
    """Creates callback to return distance between points."""
    _distances = {}
    _distances = dist_mat

    def distance_evaluator(manager, from_node, to_node):
        """Returns the manhattan distance between the two nodes"""
        return _distances[manager.IndexToNode(from_node)][manager.IndexToNode(
            to_node)]

    return distance_evaluator


def create_demand_evaluator_cvrptw(data):
    """Creates callback to get demands at each location."""
    _demands = data['demands']

    def demand_evaluator(manager, node):
        """Returns the demand of the current node"""
        return _demands[manager.IndexToNode(node)]

    return demand_evaluator


def add_capacity_constraints_cvrptw(routing, data, demand_evaluator_index):
    """Adds capacity constraint"""
    capacity = 'Capacity'
    routing.AddDimension(
        demand_evaluator_index,
        0,  # null capacity slack
        data['vehicle_capacity'],
        True,  # start cumul to zero
        capacity)


def create_time_evaluator_cvrptw(data, time_mat):
    """Creates callback to get total times between locations."""

    _total_time = {}
    _total_time = time_mat

    def time_evaluator(manager, from_node, to_node):
        """Returns the total time between the two nodes"""
        return _total_time[manager.IndexToNode(from_node)][manager.IndexToNode(
            to_node)]

    return time_evaluator


def add_time_window_constraints_cvrptw(routing, manager, data, time_evaluator_index, horizon):
    """Add Global Span constraint"""
    time = 'Time'
    horizon = horizon
    routing.AddDimension(
        time_evaluator_index,
        horizon,  # allow waiting time
        horizon,  # maximum time per vehicle
        False,  # don't force start cumul to zero since we are giving TW to start nodes
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot
    # and 'copy' the slack var in the solution object (aka Assignment) to print it
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        routing.AddToAssignment(time_dimension.SlackVar(index))
    # Add time window constraints for each vehicle start node
    # and 'copy' the slack var in the solution object (aka Assignment) to print it
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                data['time_windows'][0][1])
        routing.AddToAssignment(time_dimension.SlackVar(index))
        # Warning: Slack var is not defined for vehicle's end node
        #routing.AddToAssignment(time_dimension.SlackVar(self.routing.End(vehicle_id)))
        

# [START solution_printer]
def print_solution_cvrptw(manager, routing, assignment, total_capacity, dist_mat):  # pylint:disable=too-many-locals
    """Prints assignment on console"""
    print(f'Objective: {assignment.ObjectiveValue()}')
    time_dimension = routing.GetDimensionOrDie('Time')
    capacity_dimension = routing.GetDimensionOrDie('Capacity')
    total_distance = 0
    total_load = 0
    total_time = 0
    global weight_at_each_point
    global indexpoint_weight_at_each_point
    global Extra_weight
    weight_at_each_point = []
    Extra_weight = []
    indexpoint_weight_at_each_point = []
    for vehicle_id in range(manager.GetNumberOfVehicles()):

        weight_for_each_rider = []
        index_weight_for_each_rider = []

        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        distance = 0
        while not routing.IsEnd(index):
            load_var = capacity_dimension.CumulVar(index)
            time_var = time_dimension.CumulVar(index)
            slack_var = time_dimension.SlackVar(index)
            matr[vehicle_id].append(manager.IndexToNode(index))

            weight_for_each_rider.append(assignment.Value(load_var))
            index_weight_for_each_rider.append(manager.IndexToNode(index))

            plan_output += ' {0} Load({1}) Time({2},{3}) Slack({4},{5}) ->'.format(
                manager.IndexToNode(index),
                assignment.Value(load_var),
                assignment.Min(time_var),
                assignment.Max(time_var),
                assignment.Min(slack_var), assignment.Max(slack_var))
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            from_lo = manager.IndexToNode(previous_index)
            to_lo = manager.IndexToNode(index)
            distance+=dist_mat[from_lo][to_lo]

        indexpoint_weight_at_each_point.append(index_weight_for_each_rider)
        weight_at_each_point.append(weight_for_each_rider)

        load_var = capacity_dimension.CumulVar(index)
        time_var = time_dimension.CumulVar(index)
        slack_var = time_dimension.SlackVar(index)
        plan_output += ' {0} Load({1}) Time({2},{3})\n'.format(
            manager.IndexToNode(index),
            assignment.Value(load_var),
            assignment.Min(time_var), assignment.Max(time_var))
        plan_output += 'Distance of the route: {0}m\n'.format(distance)

        plan_output += 'Load of the route: {}\n'.format(
            assignment.Value(load_var))
        
        Extra_weight.append(total_capacity - assignment.Value(load_var))
        
        plan_output += 'Time of the route: {}\n'.format(
            assignment.Value(time_var))
        time_route[vehicle_id] = assignment.Value(time_var)
        print(plan_output)
        total_distance += distance
        total_load += assignment.Value(load_var)
        total_time += assignment.Value(time_var)
    print('Total Distance of all routes: {0}m'.format(total_distance))
    print('Total Load of all routes: {}'.format(total_load))
    print('Total Time of all routes: {0}min'.format(total_time))
    # [END solution_printer]


def get_routes(dist_mat, time_mat, num_locations, time_window, demands, num_vehicles, total_capacity, horizon):
    """Solve the Capacitated VRP with time windows."""
    # Instantiate the data problem.
    # [START data]
    data = create_data_model_cvrptw(num_locations, time_window, demands, num_vehicles, total_capacity)
    # [END data]

    # Create the routing index manager.
    # [START index_manager]
    manager = pywrapcp.RoutingIndexManager(data['num_locations'],
                                           data['num_vehicles'], data['depot'])
    
    # [END index_manager]

    # Create Routing Model.
    # [START routing_model]
    routing = pywrapcp.RoutingModel(manager)
    # [END routing_model]

    # Define weight of each edge.
    # [START transit_callback]
    distance_evaluator_index = routing.RegisterTransitCallback(
        partial(create_distance_evaluator_cvrptw(data, dist_mat), manager))

    # [END transit_callback]

    # Define cost of each arc.
    # [START arc_cost]
    routing.SetArcCostEvaluatorOfAllVehicles(distance_evaluator_index)
    # [END arc_cost]

    # Add Capacity constraint.
    # [START capacity_constraint]
    demand_evaluator_index = routing.RegisterUnaryTransitCallback(
        partial(create_demand_evaluator_cvrptw(data), manager))
    add_capacity_constraints_cvrptw(routing, data, demand_evaluator_index)
    # [END capacity_constraint]

    # Add Time Window constraint.
    # [START time_constraint]
    time_evaluator_index = routing.RegisterTransitCallback(
        partial(create_time_evaluator_cvrptw(data, time_mat), manager))
    add_time_window_constraints_cvrptw(routing, manager, data, time_evaluator_index, horizon)
    # [END time_constraint]

    
    # allow to drop nodes(by adding penalties to each node)
    for node in range(1, len(penalties)):
        pen = int(penalties[node])
        routing.AddDisjunction([manager.NodeToIndex(node)], pen)

    # Setting first solution heuristic (cheapest addition).
    # [START parameters]
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(2)
    search_parameters.log_search = True
    # search_parameters.time_limit.seconds = 5
    # [END parameters]

    global matr
    matr = [[] for j in range(num_vehicles)]
    # Solve the problem.
    # [START solve]
    solution = routing.SolveWithParameters(search_parameters)
    # [END solve]


    # Print solution on console.
    # [START print_solution]
    if solution:
        print_solution_cvrptw(manager, routing, solution, total_capacity, dist_mat)
        # return True
    # else:
        # print('No solution found!')
        # return False
    # [END print_solution]
    return matr

def first_call():
    global tot
    global num_locations 
    global num_vehicles 
    global dist_mat 
    global time_mat
    global max_time
    global time_window
    global total_capacity 
    global demands 
    global demand_copy
    global vehicle_routes
    global matr
    global new_matr 
    global new_distance_after_pickup 
    global new_distance_before_pickup 
    global time_route 
    global vehicle_time_limit
    global horizon 
    global weight_at_each_point 
    global Extra_weight 
    global indexpoint_weight_at_each_point 
    global total_dynamic_points 
    global penalties 
    global base 

        
    df = pd.read_csv('distance_matrix.csv')
    np_array = df.to_numpy()
    rows, cols = np_array.shape

    ddf = pd.read_csv('driver_data.csv')
    ddf_array = ddf.to_numpy()
    drows, dcols  = ddf_array.shape

    tot = 0

    num_locations = rows - 1
    num_vehicles = drows -1
    dist_mat = np.loadtxt(open("./distance_matrix.csv", "rb"), delimiter=",", skiprows=1,usecols=range(1,rows))
    time_mat = np.loadtxt(open("./time_matrix.csv", "rb"), delimiter=",", skiprows=1,usecols=range(1,rows))
    time_mat = time_mat/60
    max_time = 300
    time_window = [(0, 0)]
    for i in range(num_locations-1):
        time_window.append((0,max_time))

    total_capacity = 500000
    demands = [0] 
    for i in range(num_locations-1):
        demands.append(np.random.randint(1000,32000))

    demand_copy = copy.deepcopy(demands)

    vehicle_routes = [[] for j in range(num_vehicles)]
    matr = []
    new_matr = []
    new_distance_after_pickup = []
    new_distance_before_pickup = []
    time_route = [0 for j in range(num_vehicles)]

    vehicle_time_limit = [720 for j in range(num_vehicles)]

    horizon = 300

    weight_at_each_point = []
    Extra_weight = []
    indexpoint_weight_at_each_point = []

    total_dynamic_points = 0

    #calculating penalities
    penalties = []

    base = 0
    for i in range(0,num_locations):
        for j in range(0,num_locations):
            base += dist_mat[i][j]


    penalties.append(0)

    for i in range(1,num_locations):
        penalties.append(base+3*dist_mat[0][i]+2*time_mat[0][i])

    return get_routes(dist_mat, time_mat, num_locations, time_window, demands, num_vehicles, total_capacity, horizon)
    


def geojson_file(longitudes,latitudes):
    global vehicle_routes
    file = open('polygon.geojson', 'w')
    file.write('{\n  "type": "FeatureCollection",\n  "features": [\n')
    
    temp_vehicle_routes = []
    temp_latitudes = []
    temp_longitudes = []
    for vehicle in range(0,len(vehicle_routes)):
        temp = []
        for index in range(0,len(vehicle_routes[vehicle])):
            if(latitudes[vehicle_routes[vehicle][index]]>70 and latitudes[vehicle_routes[vehicle][index]]<79):
                if(longitudes[vehicle_routes[vehicle][index]]>10 and longitudes[vehicle_routes[vehicle][index]]<20):
                    temp.append(vehicle_routes[vehicle][index])
                    temp_latitudes.append(latitudes[vehicle_routes[vehicle][index]])
                    temp_longitudes.append(longitudes[vehicle_routes[vehicle][index]])
        temp_vehicle_routes.append(temp)

    vehicle_routes = temp_vehicle_routes
    longitudes = temp_longitudes
    latitudes = temp_latitudes

    for vehicle in range(0,len(vehicle_routes)):
        filename = 'polygon'+str(vehicle)+'.geojson'
        file = open(filename, 'w')
        file.write('{\n  "type": "FeatureCollection",\n  "features": [\n')

        file.write('    {\n      "type": "Feature",\n      "properties": {},\n      "geometry": {\n       "coordinates": [\n          ')
        file.write(str(latitudes[vehicle_routes[vehicle][0]]))
        file.write(',\n          ')
        file.write(str(longitudes[vehicle_routes[vehicle][0]]))
        file.write('\n        ],\n        "type": "Point"\n      }\n    },\n')
        for index in range(1,len(vehicle_routes[vehicle])):
            file.write('    {\n      "type": "Feature",\n      "properties": {},\n      "geometry": {\n       "coordinates": [\n          ')
            file.write(str(latitudes[vehicle_routes[vehicle][index]]))
            file.write(',\n          ')
            file.write(str(longitudes[vehicle_routes[vehicle][index]]))
            file.write('\n        ],\n        "type": "Point"\n      }\n    },\n')

            file.write('    {\n      "type": "Feature",\n      "properties": {},\n      "geometry": {\n        "coordinates": [\n          [\n            ')
            file.write(str(latitudes[vehicle_routes[vehicle][index]]))
            file.write(',\n            ')
            file.write(str(longitudes[vehicle_routes[vehicle][index]]))
            file.write('\n')
            file.write('          ],\n          [\n            ')
            file.write(str(latitudes[vehicle_routes[vehicle][index-1]]))
            file.write(',\n            ')
            file.write(str(longitudes[vehicle_routes[vehicle][index-1]]))
            file.write('\n          ]\n        ],\n        "type": "LineString"\n      }\n    },\n')
        file.write('  ]\n}')
        file.close()

        

def updation_after_first(latitudes,longitudes):
    global vehicle_routes
    global matr
    global tot
    global demand_copy
    global vehicle_time_limit
    print(len(matr))
    total_deliveries = 0
    for i in range(len(matr)):
        print ((matr[i]))
        total_deliveries += len(matr[i]) -1
    vehicle_routes = copy.deepcopy(matr)
    # print(vehicle_routes)
    # print(time_route)
    print("Total deliveries- ",total_deliveries)
    tot += total_deliveries
    global num_vehicles
    for vehicle in range(num_vehicles):
        vehicle_time_limit[vehicle] = vehicle_time_limit[vehicle] - time_route[vehicle]
        for index in range(1,len(vehicle_routes[vehicle])):
            if vehicle_routes[vehicle][index] < len(demands):
                demand_copy[vehicle_routes[vehicle][index]] = 700000
    print(tot)
    
    geojson_file(latitudes,longitudes)
    


def cvrptw_next(vehicleid):
    global vehicle_routes
    global matr
    global tot
    global demand_copy
    global vehicle_time_limit
    global weight_at_each_point
    global Extra_weight
    global indexpoint_weight_at_each_point
    global demands
    
    vehicles = 1
    vehicle_max_time = min(vehicle_time_limit[vehicleid],300 )
    window = [(0, 0)]
    for i in range(num_locations-1):
        window.append((0,vehicle_max_time))
    # demand = copy.deepcopy(demands)
    
    temp_weight = copy.deepcopy(weight_at_each_point)
    temp_extra = copy.deepcopy(Extra_weight)
    temp_indexpoint = copy.deepcopy(indexpoint_weight_at_each_point)
    
    for index in range(1,len(vehicle_routes[vehicleid])):
        demand_copy[vehicle_routes[vehicleid][index]] = 700000
    # print(demands)
    get_routes(dist_mat, time_mat, num_locations, window, demand_copy,vehicles, total_capacity, vehicle_max_time)

    vehicle_routes[vehicleid] = matr[0]

    print("Extra deliveries ",len(matr[0])-1)
    tot += (len(matr[0])-1)
    for i in range(1,len(vehicle_routes[vehicleid])):
        demand_copy[vehicle_routes[vehicleid][i]] = 700000
        
    vehicle_time_limit[vehicleid] = vehicle_time_limit[vehicleid] - time_route[vehicleid]
    temp_weight[vehicleid] = weight_at_each_point[0]
    temp_extra[vehicleid] = Extra_weight[0]
    temp_indexpoint[vehicleid] = indexpoint_weight_at_each_point[0]
    
    weight_at_each_point = copy.deepcopy(temp_weight)
    Extra_weight = copy.deepcopy(temp_extra)
    indexpoint_weight_at_each_point = copy.deepcopy(temp_indexpoint)
    
        
    print(tot)
    return(matr)

"""Simple Vehicles Routing Problem."""


def create_data_model_vrp(distance_mat,start,end):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distance_mat
    data['num_vehicles'] = 1
    data['starts'] = start
    data['ends'] = end
    return data


def print_solution_vrp(data, manager, routing, solution,route,distance_mat):
    """Prints solution on console."""
    global new_matr
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        plan = 'route '
        route_distance = 0
        ##route of the matrix
        temp = []
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            plan +=  ' {} -> '.format(route[manager.IndexToNode(index)])

            temp.append(route[manager.IndexToNode(index)])

            previous_index = index
            index = solution.Value(routing.NextVar(index)) 

            route_distance+=distance_mat[manager.IndexToNode(previous_index)][manager.IndexToNode(index)]
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan +=  ' {}  '.format(route[manager.IndexToNode(index)])
        plan_output += 'Distance of the route: {}m'.format(route_distance)
        print(plan_output)
        print(plan)
        new_matr.append(temp)
        max_route_distance = max(route_distance, max_route_distance)
        new_distance_after_pickup.append(max_route_distance)
    print('Maximum of the route distances: {}m\n'.format(max_route_distance))


def vrp(distance_mat,start,end,route):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model_vrp(distance_mat,start,end)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'],
                                           data['ends'])

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

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        100000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution_vrp(data, manager, routing, solution,route,distance_mat)
    else:
      print("no solution")

def distance_btw_points(dist_mat,route,src):
  print("route before: ",route)
  dist1 = 0
  for i in range(src+1,len(route)):
    dist1 = dist1 + dist_mat[route[i-1]][route[i]]

  if len(route)>1:
    dist1 = dist1 + dist_mat[route[len(route)-1]][0]
  return dist1

def time_btw_points(time_mat, route):
  time = 0
  for i in range(0,len(route)):
    time = time + time_mat[route[i-1]][route[i]]

  if len(route)>1:
    time = time + time_mat[route[len(route)-1]][0]
  return time

def dynamic_pickup(capacity):
    global new_matr
    global new_distance_after_pickup
    global new_distance_before_pickup
    global demands
    global demand_copy
    global indexpoint_weight_at_each_point
    global weight_at_each_point
    global Extra_weight 
    global matr
    global vehicle_routes
    global dist_mat
    global time_mat
    global total_dynamic_points
    
    total_dynamic_points += 1
    
    dist_mat = np.loadtxt(open("./distance_matrix.csv", "rb"), delimiter=",", skiprows=1,usecols=range(1,num_locations+1+total_dynamic_points))
    time_mat = np.loadtxt(open("./time_matrix.csv", "rb"), delimiter=",", skiprows=1,usecols=range(1,num_locations+1+total_dynamic_points))

    new_matr = []
    new_distance = []
    for j in range(0,len(dist_mat)):
        new_distance.append(np.random.randint(5000))

    pickup_id = len(dist_mat)-1
    #new distance after pickup

    new_distance_after_pickup = []
    new_distance_before_pickup = []
    max_clusters = num_vehicles

    pick_up_point_weight = capacity
    # point after which the  cluster can take the pick-up
    demands.append(0)
    demand_copy.append(0)

    allowed_points = []

    for j in range(0,max_clusters):
        find = [j,0]
        print("For cluster ",find[0])

        allowed_point = -1
        for var_point in reversed(range(len(weight_at_each_point[find[0]]))):
            if(pick_up_point_weight > (weight_at_each_point[find[0]][var_point] + Extra_weight[find[0]])):
                allowed_point = var_point
                break
        allowed_point += 1
        allowed_points.append(allowed_point)
        print("var_point",allowed_point)

        new_distance_before_pickup.append(distance_btw_points(dist_mat, vehicle_routes[find[0]],allowed_point))

        # if allowed_point < current_point:
        #   alllowed_point = current_point

        distance_mat = []

        route = vehicle_routes[find[0]][allowed_point:]
        route.append(pickup_id)
        if allowed_point != 0:
            route.insert(0,0)
        route.append(len(dist_mat))

        for row in route[:-1]:
            temp = []
            for column in route[:-1]:
                temp.append(dist_mat[row][column])
            # temp.append(new_distance[row])
            distance_mat.append(temp)
        temp = []
        # for column in route[:-1]:
        #     temp.append(new_distance[column])
        # temp.append(0)
        # distance_mat.append(temp)

        if allowed_point == 0:
            vrp(distance_mat,[0],[0],route)
        else:
            vrp(distance_mat,[1],[0],route)

    diff = [[new_distance_after_pickup[i] - new_distance_before_pickup[i],i] for i in range(len(new_distance_after_pickup))]
    diff.sort()

    ###new route checking time
    min_index = -1
    for index in range(0,num_vehicles):
        new_route = vehicle_routes[diff[index][1]][0:allowed_points[diff[index][1]]] + new_matr[diff[index][1]]
        time_taken = time_btw_points(time_mat,new_route)
        if time_taken < min(300,vehicle_time_limit[diff[index][1]]):
            min_index = diff[index][1]
            break

    print(min_index)
    Extra_weight[min_index] -= pick_up_point_weight
    print("new_route is ",new_route)

    #temp list to update the new route
    prefix_sum = 0
    temp_weight_pickup = []

    for var_point in range(len(new_route)):
        prefix_sum += demands[new_route[var_point]]
        temp_weight_pickup.append(prefix_sum)


    weight_at_each_point[min_index] = temp_weight_pickup
    indexpoint_weight_at_each_point[min_index] = new_route

    print(weight_at_each_point[min_index])
    print(indexpoint_weight_at_each_point[min_index])
    print(len(weight_at_each_point))
    
    if min_index!= -1 :
        vehicle_routes[min_index] = new_route
   
# first_call()

# updation_after_first()
     
# # dynamic_pickup(100)

# cvrptw_next(1)
# # dynamic_pickup(101)
# cvrptw_next(0)
# cvrptw_next()
# cvrptw_next()
# cvrptw_next()
