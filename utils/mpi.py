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
        if len(self.requestQueue) == 0:
            self.requestQueue = [newRequest]
            return

        # If new request has smaller timestamp than head of queue, send inquire
        if newRequest['timestamp'] < self.requestQueue[0]['timestamp']:
            self.inquire(newRequest['senderId'])

            # Wait for Relinquish or Yield
            messageListener = self.COMM.irecv(source=self.requestQueue[0]['senderID'], tag=MPI.ANY_TAG)
            message = messageListener.wait()

            if message['tag'] == MESSAGE_RELINQUISH or message['tag'] == MESSAGE_YIELD:
                self.requestQueue[0] = newRequest
                self.activeReplyReceiver = newRequest
                return

        # Insert new request to request queue sorted by timestamp ascending
        requestQueueCopy = self.requestQueue[:]
        for index, request in enumerate(self.requestQueue):
            if request['timestamp'] > newRequest['timestamp']:
                requestQueueCopy.insert(index, newRequest)
                break
            
            if index == len(self.requestQueue) - 1:
                requestQueueCopy.append(newRequest)

        self.requestQueue = requestQueueCopy[:]

    def saveReply(self, reply):
        replySenderId = reply['senderId']
        self.replySet.remove(replySenderId)

        if len(self.replySet) == 0:
            print '===== CS START ===== {}'.format(self.HOST_ID)
            print 'Working hard... | {}'.format(self.HOST_ID)
            time.sleep(3)
            self.relinquish()
            print '----- CS DONE ----- by {}'.format(self.HOST_ID)

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
                self.activeReplyReceiver = None

            if message['tag'] == MESSAGE_INQUIRE:
                if len(self.replySet) > 0:
                    self.yyield(message['senderId'], message['requesterId'])
            
            if message['tag'] == MESSAGE_YIELD:
                requester = None
                requesterIndexInQueue = None

                for index, request in enumerate(self.requestQueue):
                    if request['senderId'] == message['requesterId']:
                        requester = request
                        requesterIndexInQueue = index

                if not requester:
                    return

                self.requestQueue[requesterIndexInQueue] = self.requestQueue[0]
                self.requestQueue[0] = requester

                self.reply()
                


    def reply(self):
        if len(self.requestQueue) > 0:
            replyReceiver = self.requestQueue[0]

            if replyReceiver == self.activeReplyReceiver:
                return

            #print 'Reply: {} allows {} to enter CS'.format(self.HOST_ID, replyReceiver['senderId'])

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

            #print 'Sending REQUEST from {} to {}'.format(self.HOST_ID, receiverId)
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

            #print 'Sending RELINQUISH from {} to {}'.format(self.HOST_ID, receiverId)
            data = {
                'tag': MESSAGE_RELINQUISH,
                'senderId': self.HOST_ID,
            }

            self.COMM.isend(data, dest=receiverId, tag=MESSAGE_REQUEST)
    
    def inquire(self, requesterId):
        receiver = self.requestQueue[0]

        #print 'Sending INQUIRE from {} to {} in behalf of {}'.format(self.HOST_ID, receiver['senderId'], requesterId)
        data = {
            'tag': MESSAGE_INQUIRE,
            'senderId': self.HOST_ID,
            'requesterId': requesterId,
        }

        self.COMM.isend(data, dest=receiver['senderId'], tag=MESSAGE_INQUIRE)

    def yyield(self, destination, requesterId):
        #print 'Sending YIELD from {} to {}'.format(self.HOST_ID, destination)
        data = {
            'tag': MESSAGE_YIELD,
            'senderId': self.HOST_ID,
            'requesterId': requesterId,
        }

        self.COMM.isend(data, dest=destination, tag=MESSAGE_YIELD)
