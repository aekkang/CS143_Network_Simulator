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
        self.priority = 5
        self.link = link
        self.sender = sender

    def process():
        link.buffer_add(pkt)
        enqueue(CheckBuffer(self.start_time, self.link, self.sender))

class CheckBuffer(Event):
    def __init__(self, start_time, link, sender):
        self.start_time = start_time
        self.priority = 2
        self.link = link
        self.sender = sender

    def process():
        if self.link.buf_processing:
            return;
        else:    
            self.link.buf_processing = True
            packet = self.link.buffer_get()
            send_time = packet.size / self.link.rate + self.link.prop_delay
            enqueue(ReceivePacket(self.start_time + send_time, packet,
                self.link, self.sender))
            enqueue(BufferDoneProcessing(self.start_time + send_time, self.link))

class BufferDoneProcessing(Event):
    def __init__(self, start_time, link):
        self.start_time = start_time
        self.priority = 1
        self.link = link

    def process():
        self.link.buf_processing = False
        enqueue(CheckBuffer(self.start_time, self.link))

class ReceivePacket(Event):
    def __init__(self, start_time, packet, link, sender):
        self.start_time = start_time
        self.priority = 3
        self.packet = packet
        self.sender = sender
        self.receiver = link.get_recipient(sender.address)


