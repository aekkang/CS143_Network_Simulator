from pqueue import event_queue, enqueue, dequeue, qempty
import event
import link
class Router:
    ids = []
    
    r_map = {}

    # Links is a list of links
    def __init__(self, router_id, links):
        # IDs start from 1.
        self.address = len(Router.ids) + 1

        self.id = router_id
        Router.ids.append(self.id)

        # The routing table will be represented by a dictionary and calculated
        # using a class method.
        self.routing_table = {}
        self.calculate_table()

        self.links = links

    def calculate_table(self):
        '''
        Calculates routing table.
        '''
        pass

    def receive(self, pkt, time):
        next_link = link.Link.l_map[self.routing_table[pkt.sender.id]]
        enqueue(event.SendPacket(time, pkt, next_link, self))

    def __str__(self):
        return "<Router ID: " + str(self.id) + ", Routing table: " + \
        str(self.routing_table) +  ", Links: " + str(self.links) + ">"

    __repr__ = __str__
