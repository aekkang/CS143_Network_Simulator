from pqueue import event_queue, enqueue

class Event:
    ''' Generic Event class, default priority 3'''
    def __init__(self, start_time, priority = 3):
        self.start_time = start_time
        self.priority = priority
        
    def process(self): pass

class SendPacket(Event):
    def __init__(self, start_time, packet, link, sender):
        self.start_time = start_time
        self.priority = 5 + (1 - 1.0/(packet.number + 1))
        self.link = link
        self.packet = packet
        self.sender = sender

    def process(self):
        self.link.buffer_add((self.packet, self.sender))
        enqueue(CheckBuffer(self.start_time, self.link))

class CheckBuffer(Event):
    def __init__(self, start_time, link):
        self.start_time = start_time
        self.priority = 2
        self.link = link

    def process(self):
        if (self.link.buf_processing or self.link.buffer_empty()):
            return
        else:    
            self.link.buf_processing = True
            assert(self.link.buffer_empty() == False)
            packet, src = self.link.buffer_get()
            send_time = packet.size / self.link.rate + self.link.prop_delay
            receiver = self.link.get_receiver(src)
            enqueue(ReceivePacket(self.start_time + send_time, packet, \
                self.link, receiver))
            
            # CHECK: Need to add propogation delay?
            # + self.link.prop_delay
            enqueue(BufferDoneProcessing(self.start_time + \
                packet.size / self.link.rate, self.link))

class BufferDoneProcessing(Event):
    def __init__(self, start_time, link):
        self.start_time = start_time
        self.priority = 1
        self.link = link

    def process(self):
        self.link.buf_processing = False
        enqueue(CheckBuffer(self.start_time, self.link))

class ReceivePacket(Event):
    def __init__(self, start_time, packet, link, receiver):
        self.start_time = start_time
        self.priority = 3
        self.packet = packet
        self.link = link
        self.receiver = receiver

    def process(self):
        enqueue(CheckBuffer(self.start_time, self.link,))
        self.receiver.receive(self.packet, self.start_time)


class PacketTimeout(Event):
    def __init__(self, start_time, packet):
        self.start_time = start_time
        self.packet = packet
        self.priority = 3

    def process(self):
        self.packet.flow.handleTimeout(self.packet, self.start_time)


