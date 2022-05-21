"""
File: linkedbst.py
Author: Ken Lambert
"""

import random
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        nodes_stack = LinkedStack()

        cur_node = self._root
        while not nodes_stack.isEmpty() or cur_node is not None:
            if cur_node is not None:
                nodes_stack.push(cur_node)
                cur_node = cur_node.left
            else:
                cur_node = nodes_stack.pop()
                lyst.append(cur_node.data)
                cur_node = cur_node.right

        # def recurse(node):
        #     if node != None:
        #         recurse(node.left)
        #         lyst.append(node.data)
        #         recurse(node.right)

        # recurse(self._root)

        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root
        while node != item:
            if node is None:
                return None
            elif node.data < item:
                node = node.right
            elif node.data > item:
                node = node.left
            elif node.data == item:
                return node

        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)

        # return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            node = self._root
            while node is not None:
                if node.data < item:
                    if node.right is None:
                        node.right = BSTNode(item)
                        break
                    node = node.right
                elif node.data > item:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break
                    node = node.left

        # # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left == None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right == None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item's spot
        # else:
        #     recurse(self._root)
        # self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            elif top.right is None:
                return height1(top.left) + 1
            elif top.left is None:
                return height1(top.right) + 1
            else:
                left_sum = height1(top.left)
                right_sum = height1(top.right)
                return max(left_sum, right_sum) + 1

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(len(list(self.inorder()))+1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        res = []
        for elem in list(self.inorder()):
            if low <= elem <= high:
                res.append(elem)
        return res

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        def recursion(elements):
            if len(elements) == 0:
                return None
            mid = len(elements) // 2
            node = BSTNode(elements[mid])
            node.left = recursion(elements[:mid])
            node.right = recursion(elements[mid+1:])
            return node

        self._root = recursion(list(self.inorder()))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for elem in list(self.inorder()):
            if elem > item:
                return elem

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for num, elem in enumerate(list(self.inorder())[::-1]):
            if elem < item:
                return elem

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words_list = []
        with open(path, "r", encoding="utf-8") as file:
            for word in file:
                words_list.append(word.rstrip("\n"))

        random_words = random.sample(words_list, 10000)

        #search in list
        time_mark = time.time()
        for word in random_words:
            words_list.index(word)
        print(f"Time of searching of 10000 words in a sorted list is {time.time()-time_mark}")

        #serach in binary tree (words ordered)
        tree = LinkedBST()
        for word in words_list:
            tree.add(word)
        time_mark = time.time()
        for word in random_words:
            tree.find(word)
        print(f"Time of searching of 10000 words in ordered binary tree is {time.time()-time_mark}")

        #serach in binary tree (words random)
        tree = LinkedBST()
        random.shuffle(words_list)
        for word in words_list:
            tree.add(word)
        time_mark = time.time()
        for word in random_words:
            tree.find(word)
        print(f"Time of searching of 10000 words in unordered binary tree is {time.time()-time_mark}")

        #serach in balanced binary tree (words random)
        tree = LinkedBST()
        random.shuffle(words_list)
        for word in words_list:
            tree.add(word)
        tree.rebalance()
        time_mark = time.time()
        for word in random_words:
            tree.find(word)
        print(f"Time of searching of 10000 words in balanced unordered binary tree is {time.time()-time_mark}")

if __name__=="__main__":
    LinkedBST().demo_bst("words.txt")
