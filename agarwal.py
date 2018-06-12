import time
import math

from utils.mpi import MpiInterface as MPI
from utils.printTree import printTree
from utils.getBinaryTree import getBinaryTree, getMiddleElement
from utils.getQuorum import getQuorum

ASK_MYSELF = False
LOG_BINARY_TREE = False
LOG_QUORUM = True

# Initialize mpi
mpiInterface = MPI()

# Constants
REFRESH_INTERVAL = 0.5
NUMBER_OF_HOSTS = mpiInterface.NUMBER_OF_HOSTS
HOST_ID = mpiInterface.HOST_ID

# Create hosts vector
hosts = range(0, NUMBER_OF_HOSTS)

# Create binary tree
binary_tree = getBinaryTree(hosts)

# Print binary tree
if HOST_ID == 0 and LOG_BINARY_TREE:
    print '===== GENERATED BINARY TREE ===='
    printTree(binary_tree)
    print '=====   =====   ===== \n\n'

# Generate tree structured quorums
quorums = []
treeHeight = 2 * math.ceil((math.log(NUMBER_OF_HOSTS + 1, 2) - 1))

for i in range(0, int(treeHeight)):
    # Generate series of turns for getQuorum algorithm
    decisionVector = str(bin(i))
    decisionVector = decisionVector.replace('0b', '')

    quorum = getQuorum(binary_tree, decisionVector)
    quorums.append(quorum)

# Find my quorum
quorumSet = None
for quorum in quorums:
    if HOST_ID in quorum:
        quorumSet = quorum
        break

mpiInterface.quorumSet = quorumSet

# Prepare set of proces that need to accept request
replySet = quorumSet[:]
replySet.remove(HOST_ID)
mpiInterface.replySet = quorumSet[:] if ASK_MYSELF else replySet

# Print tree structured quorum
# print '===== QUORUM ====='
if LOG_QUORUM:
    print '{} my quorum {}\n'.format(HOST_ID, quorumSet)
    mpiInterface.barrier()

# Request access to CS
if HOST_ID < 4:
    mpiInterface.request()

while True:
    mpiInterface.listen()
    time.sleep(REFRESH_INTERVAL)
