import math

def getMiddleElement(array):
    if len(array) > 0:
        return int(math.floor(len(array) / 2))
    return -1

def buildTree(elements):
    middleElementIndex = getMiddleElement(elements)

    print 'Elements: {}'.format(elements)
    print 'Element in middle: {}'.format(elements[middleElementIndex])
    
    leftChild = None
    if middleElementIndex > 0:
        leftChild = buildTree(elements[0:middleElementIndex])

    rightChild = None
    if middleElementIndex + 1 < len(elements):
        rightChild = buildTree(elements[middleElementIndex + 1:])

    return {
        'Node': elements[middleElementIndex],
        'LeftChild': leftChild,
        'RightChild': rightChild
    }


def getBinaryTree(numberOfLeafs):
    nodesList = range(1, numberOfLeafs + 1)

    return buildTree(nodesList)