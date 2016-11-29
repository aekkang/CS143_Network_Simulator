from pqueue import event_queue, enqueue, dequeue, qempty
import event
import link
import packet

INF = 2147483647
class Router:
    PKT_SENT = 0
    PKT_ACKED = 1
    RTPKT_TIMEOUT = 5

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
        #self.calculate_table()

        self.links = [link.Link.l_map[i] for i in links]

        self.rneighbours = {}    # map of router ID -> link

        # Variables used for Bellman-Ford routing
        self.bf_round = 0
        self.bf_distvec = {}
        self.bf_updated = {}
        self.bf_changed = False
        self.sent_rtpkts = {}

    def set_rneighbours(self):
        for i in self.links:
            nbr = i.get_receiver(self)
            if isinstance(nbr, Router):
                self.rneighbours[nbr.id] = i

    def receive(self, pkt, time):
        if (isinstance(pkt, packet.RtAck)):
            self.sent_rtpkts[pkt.rtpkt] = Router.PKT_ACKED
        elif (isinstance(pkt, packet.RoutingPkt)):
            if self.bf_updated.get(pkt.sender.id, False) == False:
                ack_link = self.rneighbours[pkt.sender.id]
                rt_ack = packet.RtAck(pkt)
                enqueue(event.SendPacket(time, rt_ack, ack_link, self))
                if pkt.bf_round == self.bf_round:
                    self.update_bf(pkt.sender.id, pkt.distvec, ack_link.bf_lcost, time)
        else:
            next_link = link.Link.l_map[self.routing_table[pkt.recipient.id]]
            enqueue(event.SendPacket(time, pkt, next_link, self))    
                

    def update_bf(self, src_id, dvec, l_cost, time):
        '''
        src_id: the ID of the router this dvec is coming from
        dvec: the distance vector sent by router src_id
        l_cost: cost of link between self and src_id
        time: the current system time
        '''
        for rtr in dvec:                       # go through each router
            dist, pred = dvec[rtr]             # distance and predecessor from src_id
            cur_dist, cur_pred = self.bf_distvec.get(rtr, (INF, None))
            if dist + l_cost < cur_dist: 
                self.bf_distvec[dest] = (cur_dist + l_cost, src_id)
                self.bf_changed = True
        self.bf_updated[src_id] = True

        # If we have received routing packets from all neighbours,
        # then this cycle of updates is complete
        if len(self.bf_updated) == len(self.rneighbours):
            if self.bf_changed == False:
                # If the distance vector didn't change the BF is done
                # and we should/can update the routing table
                self.update_routing_table()
                # Reset list of what we've received routing packets from

            self.broadcast_distvec(time)

            self.bf_updated = {}
            self.bf_changed = False

    def broadcast_distvec(self, time):
        for rtr_id in self.rneighbours:
            link = self.rneighbours[rtr_id]
            dest = link.get_receiver(self)
            rtPkt = packet.RoutingPkt(self, dest, self.bf_distvec, \
                self.bf_round)
            enqueue(event.SendPacket(time, rtPkt, link, self))
            self.sent_rtpkts[rtPkt] = Router.PKT_SENT
            enqueue(event.RtPktTimeout(time + Router.RTPKT_TIMEOUT, self, rtPkt))


    def update_routing_table(self):
        # Go through distvec and set the routing table destination
        # according to the Bellman-Ford results
        for dst in self.bf_distvec:
            self.routing_table[dst] = self.bf_distvec[dst][1]

        print ("%s: updated routing table" % self.id)

    def handle_timeout(self, curr_time, rtpkt):
        '''
        Handle timeout for a routing packet
        '''
        status = self.sent_rtpkts.get(rtpkt, None)

        # If it's been sent but not acknowledged, resend.
        if status == Router.PKT_SENT:
            send_link = self.rneighbours[rtpkt.recipient.id]
            enqueue(event.SendPacket(curr_time, rtpkt, send_link, self))

        # If it's been acknowledged, remove it from the sent list.
        elif status == Router.PKT_ACKED:
            del self.sent_rtpkts[rtpkt]

        # If it's not in the set_rtpkts it has been acknowledged (probably
        # from a previous send. Do nothing.

    def reset_distvec(self):
        self.distvec = {}
        for rtr_id in self.rneighbours:
            self.distvec[rtr_id] = self.rneighbours[rtr_id].bf_lcost


    def __str__(self):
        return "<Router ID: " + str(self.id) + ", Routing table: " + \
        str(self.routing_table) +  ", Links: " + str(self.links) + ">"

    __repr__ = __str__

def reset_distvecs(time, round_no):
    for rtr_id in Router.ids:
        Router.r_map[rtr_id].bf_round = round_no
        Router.r_map[rtr_id].reset_distvec()
        Router.r_map[rtr_id].broadcast_distvec(time)

def set_rneighbours():
    for rtr_id in Router.ids:
        Router.r_map[rtr_id].set_rneighbours();