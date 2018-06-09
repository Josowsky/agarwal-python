def getQuorum(node):
    if not node:
        return []
    elif node.grantsPermissions():
        if node.leftChild:
            print '{} {}'.format(node.value, node.leftChild.value)
        return [node.value] + getQuorum(node.leftChild)
    else:
        if node.leftChild:
            print '{} {}'.format(node.value, node.leftChild.value)
        if node.rightChild:
            print '{} {}'.format(node.value, node.rightChild.value)
        left = getQuorum(node.leftChild)
        right = getQuorum(node.rightChild)
        if len(left) == 0 and len(right) == 0:
            print 'FAILED!!'
            exit(-1)
        else:
            return left + right
