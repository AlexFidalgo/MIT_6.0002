# O(2^n + 1)
# Enumerates all possible combinations of values. Removes all of the combinations whose total units exceeds the allowed weight.
# We'll use a Search Tree: we start with a route, look at our list of elements to be considered, we look at the first element of
# that list and we draw a left branch (taking that element) and a right branch (not taking that element); finally we choose the node
# (leaves) that has the highest value and meets our constraints.
# Time is based on the number of nodes generated; the number of levels is the number of items + 1 (at each level of the tree we are 
# deciding to take or not take an item). The number of nodes at level i is 2^i; if there are n items, the number of nodes is
# sum(i=0, i=n)2^i; O(2^n + 1).
# An obvious optimization: don't explore parts of the tree that violate constraint (e.g., too many calories) - this does not affect
# the complexity
# Very slow solution for large number (it's exponential)

class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w
    def getValue(self):
        return self.value
    def getCost(self):
        return self.calories
    def density(self):
        return self.getValue()/self.getCost()
    def __str__(self):
        return self.name + ': <' + str(self.value)\
                 + ', ' + str(self.calories) + '>'

def buildMenu(names, values, calories):
    menu = []
    for i in range(len(values)):
        menu.append(Food(names[i], values[i],
                          calories[i]))
    return menu

def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
         keyFunction maps elements of Items to numbers"""
    itemsCopy = sorted(items, key = keyFunction,
                       reverse = True)
    result = []
    totalValue, totalCost = 0.0, 0.0
    for i in range(len(itemsCopy)):
        if (totalCost+itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)

def testGreedy(items, constraint, keyFunction):
    taken, val = greedy(items, constraint, keyFunction)
    print('Total value of items taken =', val)
    for item in taken:
        print('   ', item)

def testGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits,
               lambda x: 1/Food.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.density)

def maxVal(toConsider, avail):
    """Assumes toConsider a list of items, avail a weight
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the items of that solution"""
    if toConsider == [] or avail == 0:
        result = (0, ()) #this function doesn't actually build a search tree; the result variable records the best solution found so far
    elif toConsider[0].getCost() > avail:
        #Explore right branch only
        result = maxVal(toConsider[1:], avail)
    else:
        nextItem = toConsider[0]
        #Explore left branch
        withVal, withToTake = maxVal(toConsider[1:],
                                     avail - nextItem.getCost())
        withVal += nextItem.getValue()
        #Explore right branch
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    return result

def testMaxVal(foods, maxUnits, printItems = True):
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = maxVal(foods, maxUnits)
    print('Total value of items taken =', val)
    if printItems:
        for item in taken:
            print('   ', item)

names = ['wine', 'beer', 'pizza', 'burger', 'fries',
         'cola', 'apple', 'donut', 'cake']
values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]
foods = buildMenu(names, values, calories)

testGreedys(foods, 750)
print('')
testMaxVal(foods, 750)

import random

def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
                          random.randint(1, maxVal),
                          random.randint(1, maxCost)))
    return items

#for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45):
#    print('Try a menu with', numItems, 'items')
#    items = buildLargeMenu(numItems, 90, 250)
#    testMaxVal(items, 750, False)  



def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

#for i in range(121):
#    print('fib(' + str(i) + ') =', fib(i))

# DYNAMIC PROGRAMMING

# The previous example calculates the same thing (same n) over and over again. We can optimize it. We store 
# previously computed results in a dictionary (works in constant time). We are trading time for space.
# memorandum: "thing to be recorded"


def fastFib(n, memo = {}):
    """Assumes n is an int >= 0, memo used only by recursive calls
       Returns Fibonacci of n"""
    if n == 0 or n == 1:
        return 1
    try:
        return memo[n]
    except KeyError:
        result = fastFib(n-1, memo) + fastFib(n-2, memo)
        memo[n] = result
        return result

#for i in range(121):
#    print('fib(' + str(i) + ') =', fastFib(i))

# Memoization (dynamic programming) works when we have:
# - Optimal Substructure: a globally optimal solution can be found by combining optimal solutions to local
# subproblems
# - Overlapping Problems: finding an optimal solution involves solving the same problem multiple times

# The knapsack problem has optimal substructure, but no overlapping problems (we don't face the same decision over
# and over again). However, if the menu happens to have more than one of the same item, we see more than one node
# solving the same problem. Actually if we have the same items left to choose and the same remaining calories, then
# we have the same problem.

def fastMaxVal(toConsider, avail, memo = {}):
    """Assumes toConsider a list of subjects, avail a weight
         memo supplied by recursive calls
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the subjects of that solution"""
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
    elif toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        #Explore right branch only
        result = fastMaxVal(toConsider[1:], avail, memo)
    else:
        nextItem = toConsider[0]
        #Explore left branch
        withVal, withToTake =\
                 fastMaxVal(toConsider[1:],
                            avail - nextItem.getCost(), memo)
        withVal += nextItem.getValue()
        #Explore right branch
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
                                                avail, memo)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result
    return result

# Incredibly faster than MaxVal. Running time of fastMaxVal is governed by number of distinct pairs <toConsider,
# avail>. 

def testMaxVal(foods, maxUnits, algorithm, printItems = True):
    print('Menu contains', len(foods), 'items')
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = algorithm(foods, maxUnits)
    if printItems:
        print('Total value of items taken =', val)
        for item in taken:
            print('   ', item)
          
#for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
#    items = buildLargeMenu(numItems, 90, 250)
#    testMaxVal(items, 750, fastMaxVal, True)