from mpi4py import MPI

MESSAGE_REQUEST = 1

class MpiInterface:
    def __init__(self):
        self.COMM = MPI.COMM_WORLD
        self.NUMBER_OF_HOSTS = self.COMM.Get_size()
        self.HOST_ID = self.COMM.Get_rank()

    def request(hostId, quorumSet):
        for host in quorumSet:
            pass
            # send request message from sender to receiver