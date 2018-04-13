#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])


def greedy(items, capacity):
    '''
    The stock, greedy solution.
    Returns: str
    '''
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def dynamic_programming(items, capacity):
    '''
    Dyanmic programming solution.
    Args:
        items: Item namedtuple
        capacity:  int

    Returns:
        str
    '''
    arr = [[0 for _ in range(len(items)+1)]
              for _ in range(capacity+1)]

    print('items', items)
    print('arr', arr)
    print('num items: ', len(items))
    print('capacity: ', capacity)
    print(items)

    value = 0
    weight = 0

    def oracle(capacity, nth_item):
        '''
        Args:
            items:
            capacity:

        Returns:
        '''
        next_item = items[nth_item-1]
        weight = arr[capacity][nth_item] + next_item.weight
        print('weight: '+str(weight), 'capacity: '+str(capacity))

        # if items[nth_item-1] fits
        if weight <= capacity:
            try:
                best = max(
                    arr[capacity][nth_item-1],
                    next_item.value + arr[capacity - next_item.weight][nth_item-1]
                )
                print('best', best)
            except:
                # out of bounds
                best = 0

        # if it doesn't fit
        else:
            try:
                best = arr[capacity][nth_item-1]
                print('did not fit, best is...', best)
            except IndexError:
                # out of bounds...
                best = 0

        return best

    # fill the array
    for cap in range(1, capacity+1):
        for item_idx in range(1, len(items)+1):
            print('capacity: '+str(cap), 'item_idx: '+str(item_idx))
            arr[cap][item_idx] = oracle(capacity=cap, nth_item=item_idx)
            print('arr value', arr[cap][item_idx])
            print()

    def traceback(arr):
        """Find the items selected."""
        assert len(arr) > 0
        assert len(arr[0]) > 0
        print('caps len', len(arr))
        print('items len', len(arr[0]))

        items_selected = []

        rem_capacity = len(arr)-1
        item_num = len(arr[0])-1
        last_item_picked = arr[rem_capacity][item_num]

        item_arr = [0] * len(arr[0])

        for item in reversed(range(item_num)):
            prev_item = arr[rem_capacity][item-1]

            print('last item', last_item_picked)
            print('prev item', prev_item)
            print('rem capacity', rem_capacity)
            print()

            # check if item was picked
            if last_item_picked == prev_item or rem_capacity <= 0:
                continue
            else:
                # confirm we could pick it
                if rem_capacity - items[item].weight >= 0:
                    last_item_picked = prev_item
                    rem_capacity -= items[item].weight
                    items_selected.append(items[item])
                    item_arr[item] = 1
        print('items selected', items_selected)
        print('items arr', item_arr)
        return ' '.join(map(str, item_arr)) #item_arr


    print('results array', arr)
    results = traceback(arr)

    return results


def solve_it(input_data, func=greedy):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))


    return func(items=items, capacity=capacity)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data, func=dynamic_programming))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

