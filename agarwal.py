from utils.mpi import MpiInterface
from utils.printTree import printTree
from utils.getBinaryTree import getBinaryTree, getMiddleElement
from utils.getQuorum import getQuorum

# Initialize mpi
mpiInterface = MpiInterface()

# Constants
NUMBER_OF_HOSTS = mpiInterface.NUMBER_OF_HOSTS
HOST_ID = mpiInterface.HOST_ID

# # Create hosts vector
# hosts = range(0, NUMBER_OF_HOSTS)

# Put our process in the middle of hosts vector
middleElementIndex = getMiddleElement(hosts)
hosts[HOST_ID] = hosts[middleElementIndex]
hosts[middleElementIndex] = HOST_ID

# Create binary tree
binary_tree = getBinaryTree(hosts)

# Print binary tree
print '===== GENERATED BINARY TREE ===='
printTree(binary_tree)
print '=====   =====   ===== \n\n'

# Get tree structured quorum
print '===== QUORUM ====='
print '{}\n'.format(getQuorum(binary_tree))

# Request access to CS
pass

# for thread in threads:
#    thread.start()
