DIRECTION_LEFT = '0'
DIRECTION_RIGHT = '1'

DEBUG_GET_QUORUM = False

def getQuorum(node, decisionVector, step=1):
    if not node:
        return []
    elif node.grantsPermissions():
        direction = DIRECTION_LEFT

        if len(decisionVector) > step - 1:
            direction = decisionVector[-step]

        if direction == DIRECTION_LEFT:
            if DEBUG_GET_QUORUM: print '{} left {}'.format(node.value, decisionVector)
            step += 1
            return [node.value] + getQuorum(node.leftChild, decisionVector, step)
        if direction == DIRECTION_RIGHT:
            if DEBUG_GET_QUORUM: print '{} right {}'.format(node.value, decisionVector)
            step += 1
            return [node.value] + getQuorum(node.rightChild, decisionVector, step)
    else:
        left = getQuorum(node.leftChild, decisionVector, step)
        right = getQuorum(node.rightChild, decisionVector, step)

        if len(left) == 0 and len(right) == 0:
            print 'FAILED TO CREATE QUORUM!!'
            exit(-1)
        else:
            step += 1
            return left + right
