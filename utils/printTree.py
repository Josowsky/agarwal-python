def printTree(node):
    if not node:
        return ''
    node.printNode()
    printTree(node.leftChild)
    printTree(node.rightChild)
