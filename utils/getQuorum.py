def getQuorum(node):
    if not node:
        return []
    elif node.grantsPermissions():
        return [node.value] + getQuorum(node.leftChild)
    else:
        left = getQuorum(node.leftChild)
        right = getQuorum(node.rightChild)

        if len(left) == 0 and len(right) == 0:
            print 'FAILED TO CREATE QUORUM!!'
            exit(-1)
        else:
            return left + right
