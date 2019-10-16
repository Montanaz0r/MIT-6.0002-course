from ps1_partition import get_partitions
import time

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
    data_file = open(filename, 'r')
    cows_dict = {}
    for line in data_file:
        name, weight = line.split(',')
        cows_dict[name] = int(weight)
    data_file.close()
    return cows_dict

# Problem 2
def greedy_cow_transport(cows, limit=10):
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
    # creating list of tuples, sorted by weight from cows dict.
    sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    result = []   # creating list where results will be appended.
    trip = 0   # increasing with each trip.
    while len(sorted_cows) > 0:  # after there is no cow left, the job is done.
        trip_limit = limit   # sets the initial limit for the trip.
        result.append([])   # initiating trip sub-list.
        removed_cows = []  # creating a list with indexes of cows that were already assigned to the trip.
        for cow in sorted_cows:
            if cow[1] <= trip_limit:   # checking if weight of cow meets current constraint.
                result[trip].append(cow[0])
                removed_cows.append(sorted_cows.index(cow))
                trip_limit -= cow[1]   # updating the limit for current trip.
        trip += 1
        for cow_index in sorted(removed_cows, reverse=True):
            sorted_cows.pop(cow_index)
    return result

# Problem 3
def brute_force_cow_transport(cows, limit=10):
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
    cows_by_names = list(cows.keys())   # creating list that contains only cows names (keys from cow dictionary).
    copy_cows = cows   # creating copy of cow dictionary
    result = []   # final result will be appended to this list.
    for partition in get_partitions(cows_by_names):   # iterating over sets created by get_partitions algorithm.
        weight_over_limit = False   # default is False.
        for sublist in partition:
            weight = 0
            for cow in sublist:
                weight += copy_cows[cow]
            if weight > limit:
                weight_over_limit = True   # True after sum of weights exceeds limit.
                break   # We can stop iterating over partition, since the solution does not meet constraints.
        if weight_over_limit is True:
            continue
        elif len(result) == 0 or len(result) > len(partition):
            result = partition   # partition is our new result if there was no valid solution before, or the new one
                                 # is better (shorter) than the one stored in result.
    return result

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
    cows_dataset = 'ps1_cow_data.txt'   # file that contains data
    cows = load_cows(cows_dataset)
    # testing greedy algorithm first
    start = time.time()
    result = greedy_cow_transport(cows)
    end = time.time()
    print(f'Execution time for greedy algorithm was {end - start}.')
    print(f'Problem was solved within {len(result)} trips.')
    # testing brute force algorithm afterwards
    start = time.time()
    result = brute_force_cow_transport(cows)
    end = time.time()
    print(f'Execution time for brute force algorithm was {end - start}.')
    print(f'Problem was solved within {len(result)} trips.')

if __name__ == '__main__':
    compare_cow_transport_algorithms()