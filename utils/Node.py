class Node:
    def __init__(self, value, leftChild, rightChild):
        self.value = value
        self.leftChild = leftChild
        self.rightChild = rightChild
    
    def grantsPermissions(self):
        return True

    def printNode(self):
        leftChild = None
        rightChild = None
        if self.leftChild:
            leftChild = self.leftChild.value
        if self.rightChild:
            rightChild = self.rightChild.value
        print '[{}] <- [{}] -> [{}] \n'.format(leftChild, self.value, rightChild)
