from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])
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
    selected = [item for item, selected in zip(items, selections)
                    if selected]
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
        # it's a leaf if we're out ot items,
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


def traverse(items, capacity):
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

            result += [curr.selected.selections, curr.selected.val]
            result += [curr.not_selected.selections, curr.not_selected.val]

    return result


if __name__ == '__main__':
    print('making a tree')

    # test case
    items = [Item(index=0, value=8, weight=4),
             Item(index=1, value=10, weight=5),
             Item(index=2, value=15, weight=8),
             Item(index=3, value=4, weight=3)]

    selections = [0 for _ in items]

    result = traverse(items=items, capacity=11)
    print(result)