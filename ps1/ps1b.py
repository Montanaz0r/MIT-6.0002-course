#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    sorted_eggs = sorted(egg_weights, reverse=True)   # sorting weights of eggs in descending order.
    number_of_eggs = 0   # counter for the number of eggs that algorithm will take, starts at 0.
    remaining_weight = target_weight   # available weight, will be decreased after some amount of eggs has been taken.
    for index in range(len(sorted_eggs)):
        eggs_to_take = remaining_weight // sorted_eggs[index]
        number_of_eggs += eggs_to_take
        remaining_weight -= eggs_to_take * sorted_eggs[index]
        if remaining_weight == 0:   # no point in looping through lighter eggs if there is no more remaining weight.
            break
    return number_of_eggs

if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    egg_weights = (2, 3, 5, 10, 50)
    n = 998
    print("Egg weights = (2, 3, 5, 50)")
    print("n = 998")
    print("Expected ouput: 25 (19 * 50 + 4 * 10 + 1 * 5 + 1 * 3 = 998)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    egg_weights = (3, 5, 10, 20)
    n = 543
    print("Egg weights = (3, 5, 10, 20)")
    print("n = 545")
    print("Expected ouput: 28 (27 * 20 + 1 * 5 = 28)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()