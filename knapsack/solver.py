#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])


#
# Greedy
#
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


#
# Dynamic Programming
#
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


#
# Relaxation, Branch & Bound
#
from copy import deepcopy


def relaxation_heuristic(capacity, items, selections):
    '''Calculate the relaxed heuristic value.'''
    # add items until next item would go over
    # then grab a fraction of next item, such that it would fill the knapsack
    # i.e. --> that's the optimistic best you could ever hope to do, in this branch
    # calculate the 'density' of each item --> value/weight
    # select N densest full items; and fraction of next, until full
    # sum of values is the estimation

    # order the items by density
    selected = [item for item, selected in zip(items, selections) if selected]
    ordered = list(reversed(sorted(selected, key=lambda x: x.value/x.weight)))
    print('ordered', ordered)

    # calculate the heuristic value
    value = 0

    for item in ordered:
        # if we have capacity, take the whole item
        if capacity > item.weight and selections[item.index]:
            value += item.value
            capacity -= item.weight

        # else take a fraction of the item
        else:
            fraction = float(capacity)/float(item.weight)
            value += fraction * item.value

    return value


class Tree(object):

    def __init__(self, parent, item_index, items, selections, val, room, estimate, best):
        self.parent = parent
        self.item_index = item_index
        self.items = items
        self._selected = None
        self._not_selected = None
        self.selections = selections
        self.val = val
        self.room = room
        self.estimate = estimate
        self.best = best

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, item):
        my_index = item.index
        my_selections = deepcopy(self.selections)
        my_selections[my_index] = 1
        my_val = self.val + item.value
        my_room = self.room - item.weight

        print()
        print('---selected---')
        print('item passed in', item)
        print('my_index', my_index)
        print('my_val', my_val)
        print('my_room', my_room)
        print('selections', my_selections)
        my_estimate = relaxation_heuristic(capacity=my_room,
                                           items=self.items,
                                           selections=my_selections)

        print()


        my_best = my_estimate if my_estimate > self.best else self.best

        self._selected = Tree(parent=self,
                              item_index=my_index+1,
                              items=self.items,
                              selections=my_selections,
                              val=my_val,
                              room=my_room,
                              estimate=my_estimate,
                              best=my_best)

    @property
    def not_selected(self):
        return self._not_selected

    @not_selected.setter
    def not_selected(self, item):
        my_index = item.index
        my_selections = deepcopy(self.selections)
        my_selections[my_index] = 0
        print()
        print('---not selected---')
        print('item passed in', item)
        print('my_index', my_index)
        print('my_val', self.val)
        print('my_room', self.room)
        print('selections', my_selections)
        my_estimate = relaxation_heuristic(capacity=self.room,
                                           items=self.items,
                                           selections=my_selections)

        my_best = my_estimate if my_estimate > self.best else self.best

        self._not_selected = Tree(parent=self,
                                  item_index=my_index+1,
                                  items=self.items,
                                  selections=my_selections,
                                  val=self.val,
                                  room=self.room,
                                  estimate=my_estimate,
                                  best=my_best)

    def has_room(self, item):
        return self.room - item.weight > 0

    def estimate(self, item):
        my_selections = self.selections
        my_selections[item.index] = 1
        my_room = self.room - item.capacity

        my_estimate = relaxation_heuristic(capacity=my_room,
                                           items=self.items,
                                           selections=my_selections)
        return my_estimate

    def is_leaf(self):
        # it's a leaf if we're out of items,
        # or have no room
        try:
            return self.item_index >= len(self.items) or \
                   not self.has_room(item=self.items[self.item_index])
        # except case for root, when we don't have an index yet
        except:
            return False

    def is_pruned(self):
        # if the optimistic estimate is worse than our best seen,
        # then there's no reason to keep traversing
        return self.estimate < self.best


def branch_and_bound(items, capacity):
    # set base values
    starting_selections = [0 for _ in items]
    first_estimate = relaxation_heuristic(capacity=capacity,
                                          items=items,
                                          selections=starting_selections)
    root = Tree(parent=None,
                item_index=None,
                items=items,
                selections=starting_selections,
                val=0,
                room=capacity,
                estimate=first_estimate,
                best=first_estimate)

    # perform traversal
    path, result = [root], []
    while path:
        curr = path.pop()
        if not curr.is_leaf() and not curr.is_pruned():

            # generate the next level of tree
            idx = curr.item_index or 0
            current_item = curr.items[idx]
            curr.selected = current_item
            curr.not_selected = current_item

            path += [curr.selected, curr.not_selected]

            result.append([curr.selected.selections, curr.selected.val])
            result.append([curr.not_selected.selections, curr.not_selected.val])

    ordered_results = list(reversed(sorted(result, key=lambda x: x[1])))
    selections = ordered_results[0][0]
    value = ordered_results[0][1]

    print()
    output_data = str(value) + ' 0\n'
    output_data += ' '.join(map(str, selections))
    return output_data


#
# Solver
#
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
        print(solve_it(input_data, func=branch_and_bound))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

