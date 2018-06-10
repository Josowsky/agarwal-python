from Node import Node
import math


def getMiddleElement(array):
    if len(array) > 0:
        return int(math.floor(len(array) / 2))
    return -1


def getBinaryTree(elements):
    middleElementIndex = getMiddleElement(elements)

    leftChild = None
    if middleElementIndex > 0:
        leftChild = getBinaryTree(elements[0:middleElementIndex])

    rightChild = None
    if middleElementIndex + 1 < len(elements):
        rightChild = getBinaryTree(elements[middleElementIndex + 1:])

    return Node(
        elements[middleElementIndex],
        leftChild,
        rightChild,
    )
