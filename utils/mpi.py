from mpi4py import MPI
import time

MESSAGE_REQUEST = 1
MESSAGE_REPLY = 2

class MpiInterface:
    def __init__(self):
        self.COMM = MPI.COMM_WORLD
        self.NUMBER_OF_HOSTS = self.COMM.Get_size()
        self.HOST_ID = self.COMM.Get_rank()

        self.requestQueue = []
        self.quorumSet = []

    def addToRequestQueue(self, newRequest):
        if len(self.requestQueue) == 0:
            self.requestQueue = [newRequest]
            return

        for index, request in enumerate(self.requestQueue):
            if request['timestamp'] > newRequest['timestamp']:
                self.requestQueue.insert(index, newRequest)
                break
            
            if index == len(self.requestQueue - 1):
                self.requestQueue.append(newRequest)

    def saveReply(self, reply):
        replySenderId = reply['senderId']
        self.quorumSet.remove(replySenderId)

        if len(self.quorumSet) == 0:
            print 'I can enter the CS!! {}'.format(self.HOST_ID)

    def listen(self):
        self.reply()

        if self.COMM.iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG):
            messageListener = self.COMM.irecv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
            message = messageListener.wait()

            if message['senderId'] == self.HOST_ID:
                return
            
            if message['tag'] == MESSAGE_REQUEST:
                self.addToRequestQueue(message)

            if message['tag'] == MESSAGE_REPLY:
                self.saveReply(message)

    def reply(self):
        if len(self.requestQueue) > 0:
            replyReceiver = self.requestQueue.pop(0)
            print 'Reply: {} allows {} to enter CS'.format(self.HOST_ID, replyReceiver['senderId'])

            data = {
                'tag': MESSAGE_REPLY,
                'senderId': self.HOST_ID,
                'timestamp': time.time()
            }

            self.COMM.isend(data, dest=replyReceiver['senderId'], tag=MESSAGE_REPLY)

    def request(self, senderId, quorumSet):
        for receiverId in quorumSet:
            if receiverId == self.HOST_ID:
                continue

            print 'Sending REQUEST from {} to {}'.format(senderId, receiverId)
            data = {
                'tag': MESSAGE_REQUEST,
                'senderId': senderId,
                'timestamp': time.time()
            }

            self.COMM.isend(data, dest=receiverId, tag=MESSAGE_REQUEST)