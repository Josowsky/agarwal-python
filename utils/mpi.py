from mpi4py import MPI
import time

MESSAGE_REQUEST = 1

class MpiInterface:
    def __init__(self):
        self.COMM = MPI.COMM_WORLD
        self.NUMBER_OF_HOSTS = self.COMM.Get_size()
        self.HOST_ID = self.COMM.Get_rank()

    def listen(self):
        print 'Listening to any mesage at {}'.format(self.HOST_ID)

        messageListener = self.COMM.irecv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        message = messageListener.wait()
        
        print 'Received {} from {} to {}'.format(message['tag'], message['senderId'], self.HOST_ID)
        # print 'Received {} from {} to {}'.format(1, self.HOST_ID) 

    def request(self, senderId, quorumSet):
        for receiverId in quorumSet:
            print 'Sending REQUEST from {} to {}'.format(senderId, receiverId)
            data = {
                'tag': MESSAGE_REQUEST,
                'senderId': senderId,
                'timestamp': time.time()
            }

            req = self.COMM.isend(data, dest=receiverId, tag=MESSAGE_REQUEST)