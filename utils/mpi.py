from mpi4py import MPI
import time

MESSAGE_REQUEST = 1
MESSAGE_REPLY = 2
MESSAGE_RELINQUISH = 3
MESSAGE_INQUIRE = 4
MESSAGE_YIELD = 5

class MpiInterface:
    def __init__(self):
        self.COMM = MPI.COMM_WORLD
        self.NUMBER_OF_HOSTS = self.COMM.Get_size()
        self.HOST_ID = self.COMM.Get_rank()

        # List of nodes that requested access to the CS
        self.requestQueue = []

        # Process that curently has my reply
        self.activeReplyReceiver = None

        # List of necessary replys to required to enter CS
        # If this list is empty then you can enter CS
        self.replySet = []

        # My quorum
        self.quorumSet = []

    def addToRequestQueue(self, newRequest):
        newRequestIndexInQueue = None

        if len(self.requestQueue) == 0:
            newRequestIndexInQueue = 0
            self.requestQueue = [newRequest]
            return

        for index, request in enumerate(self.requestQueue):
            if request['timestamp'] > newRequest['timestamp']:
                newRequestIndexInQueue = index
                self.requestQueue.insert(index, newRequest)
                break
            
            if index == len(self.requestQueue - 1):
                newRequestIndexInQueue = len(self.requestQueue)
                self.requestQueue.append(newRequest)

        # If new request has smaller timestamp, send inquire
        if newRequestIndexInQueue > 0:
            self.inquire()

    def saveReply(self, reply):
        replySenderId = reply['senderId']
        self.replySet.remove(replySenderId)

        if len(self.replySet) == 0:
            print 'I can enter the CS!! {}'.format(self.HOST_ID)
            print 'Working hard... | {}'.format(self.HOST_ID)
            time.sleep(3)
            self.relinquish()

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

            if message['tag'] == MESSAGE_RELINQUISH:
                self.requestQueue.pop(0)

            if message['tag'] == MESSAGE_INQUIRE:
                if len(self.replySet) > 0:
                    pass


    def reply(self):
        if len(self.requestQueue) > 0:
            replyReceiver = self.requestQueue[0]

            if replyReceiver == self.activeReplyReceiver:
                return

            print 'Reply: {} allows {} to enter CS'.format(self.HOST_ID, replyReceiver['senderId'])

            data = {
                'tag': MESSAGE_REPLY,
                'senderId': self.HOST_ID,
            }

            self.activeReplyReceiver = replyReceiver
            self.COMM.isend(data, dest=replyReceiver['senderId'], tag=MESSAGE_REPLY)

    def request(self):
        for receiverId in self.replySet:
            if receiverId == self.HOST_ID:
                continue

            print 'Sending REQUEST from {} to {}'.format(self.HOST_ID, receiverId)
            data = {
                'tag': MESSAGE_REQUEST,
                'senderId': self.HOST_ID,
                'timestamp': time.time()
            }

            self.COMM.isend(data, dest=receiverId, tag=MESSAGE_REQUEST)

    def relinquish(self):
        for receiverId in self.quorumSet:
            if receiverId == self.HOST_ID:
                continue

            print 'Sending RELINQUISH from {} to {}'.format(self.HOST_ID, receiverId)
            data = {
                'tag': MESSAGE_RELINQUISH,
                'senderId': self.HOST_ID,
            }

            self.COMM.isend(data, dest=receiverId, tag=MESSAGE_REQUEST)
    
    def inquire(self):
        receiver = self.requestQueue[0]

        print 'Sending INQUIRE from {} to {}'.format(self.HOST_ID, receiver['senderId)'])
        data = {
            'tag': MESSAGE_INQUIRE,
            'senderId': self.HOST_ID,
        }

        self.COMM.isend(data, dest=receiver['senderId'], tag=MESSAGE_INQUIRE)

    def yyield(self, destination):
        print 'Sending YIELD from {} to {}'.format(self.HOST_ID, destination)
        data = {
            'tag': MESSAGE_YIELD,
            'senderId': self.HOST_ID,
        }

        self.COMM.isend(data, dest=destination, tag=MESSAGE_YIELD)
