"""
This module implements LRU cache data structure.

Insertion, retrieval and querying for most recent 
and oldest key-value pair happen in O(1) time.

Implementing this data structure costs O(min(num_keys, max_size)) space.

The key-value pairs are implemented as nodes in a doubly linked list.
If we know the position of the node with the relevant key in O(1) time, 
then updating its value and/or promoting it as the most recent costs 
O(1) time as well.

To locate and access the node in O(1) time, I use a HashMap that maps 
keys to nodes.

For O(1) lookup of most recent node and oldest node, I use node pointers
to the oldest used node and the most recently used node.
"""


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = self.next = None


class LRUCache:
    def __init__(self, max_size=None):
        self.max_size = max_size or 1
        self.key_to_node = {}
        self.oldest = self.most_recent = None

    def insert_key_value_pair(self, key, value):  # O(1) time;
        if key in self.key_to_node:  #  O(1) time avg;
            node = self.key_to_node[key]
            node.value = value
            self._update_order_existing_node(node)  # O(1) time;
        else:
            # create new node;
            node = Node(key, value)
            node.prev = self.most_recent
            if node.prev:
                node.prev.next = node
            self.most_recent = node
            if not self.oldest:
                self.oldest = node
            # add new node to the dict;
            self.key_to_node[key] = node
        
        # see if deletion needed;
        if len(self.key_to_node) > self.max_size:
            temp = self.oldest
            self.oldest = self.oldest.next
            self.oldest.prev = None
            del self.key_to_node[temp.key]
            del temp

    def get_value(self, key):  # O(1) time;
        if key in self.key_to_node:  # O(1) time avg;
            node = self.key_to_node[key]
            self._update_order_existing_node(node)  # O(1) time;
            return node.value
        return None

    def get_most_recent_key(self):  # O(1) time;
        return self.most_recent.key

    def get_oldest_key(self):  # O(1) time;
        return self.oldest.key

    def _update_order_existing_node(self, node):  # O(1) time;
        # if node is most recent already, no need to change order;
        if node != self.most_recent:  # 2 or more nodes in linked list;
            if node.prev:  # internal node -> 3 or more nodes;
                node.prev.next = node.next
            else:  # node is oldest
                self.oldest = node.next
            node.next.prev = node.prev
            node.prev = self.most_recent
            node.next = None
            self.most_recent.next = node
            self.most_recent = node


if __name__ == "__main__":
    cache = LRUCache(max_size=4)
    test_input = [
                ('insert', ('a', 1)),
                ('insert', ('b', 2)),
                ('insert', ('c', 3)),
                ('insert', ('d', 4)),
                ('get_value', ('a',)),
                ('get_value', ('b',)),
                ('get_value', ('c',)),
                ('get_value', ('d',)),
                ('insert', ('e', 5)),
                ('get_value', ('a',)),
                ('get_value', ('b', )),
                ('most_recent', ()),
                ('oldest', ()),
            ]
    expected = [None] * 4 + [1, 2, 3, 4] + [None] * 2 + [2] + ['b', 'c']
    for todo, ans in zip(test_input, expected):
        if 'insert' == todo[0]:
            res = cache.insert_key_value_pair(*todo[-1])
        elif 'get_value' == todo[0]:
            res = cache.get_value(*todo[-1])
        elif 'most_recent' == todo[0]:
            res = cache.get_most_recent_key()
        elif 'oldest' == todo[0]:
            res = cache.get_oldest_key()
        assert res == ans
        print(todo, res, ans, sep='\n', end='\n\n')

