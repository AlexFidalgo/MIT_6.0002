###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

# import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    d = {}
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            line = line.split(",") 
            d[line[0]] = int(line[1]) 
    return d

# filename = 'ps1_cow_data.txt'
# dic = load_cows(filename)

def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b

def get_partitions(set_):
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]
        
# for partition in get_partitions([1,2,3]):
#     print(partition)


filename = 'ps1_cow_data.txt'
dic = load_cows(filename)

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows2 = dict(cows)
    trips = []
    trips_final = []
    weight = 0
    while bool(cows2) == True:
        for item,value in sorted(cows2.items(), key = lambda item: -item[1]):
            if value + weight <= limit:
                trips.append(item)
                weight = weight + value
                del cows2[item]
        weight = 0
        trips_final.append(trips)
        trips = []
    return trips_final

# filename = 'ps1_cow_data.txt'
# dic = load_cows(filename)
# dic = {'Jesse': 6, 'Maybel': 3, 'Callie': 2, 'Maggie': 5}
# lis = greedy_cow_transport(dic)

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # for key, value in cows.items()
    min_num_trips = len(cows)
    best_partition = []
    for partition in get_partitions(list(dic.keys())):
        print("\npartition atual: ", partition)
        max_weight = 0
        for trip in partition:
            current_weight = 0
            for cow in trip:
                current_weight = current_weight + cows[cow]
                print(current_weight)
            if current_weight >= max_weight:
                max_weight = current_weight
        if max_weight > limit:
            continue
        num_trips = len(partition)
        print("num_trips: ", num_trips)
        print("min_num_trips: ", min_num_trips)
        if num_trips <= min_num_trips:
            min_num_trips = num_trips
            best_partition = partition
    return best_partition
        
    
filename = 'ps1_cow_data.txt'
dic = load_cows(filename)
dic = {'Jesse': 6, 'Maybel': 3, 'Callie': 2, 'Maggie': 5}
lis = brute_force_cow_transport(dic)
print("Brute Force:\n", lis)

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass
