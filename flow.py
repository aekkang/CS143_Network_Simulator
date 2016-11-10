class Flow:

    f_map = {}

    def __init__(self, flow_id, source, destination, data_amt, start_time):
        self.id = flow_id
        self.source = source
        self.destination = destination
        self.data_amt = data_amt
        self.start_time = start_time

    def __str__(self):
        return "<Flow ID: " + str(self.id) + ", Source: " + str(self.source) +  \
            ", Destination: " + str(self.destination) + ", Data Amount: " +  \
            str(self.data_amt) + ", Start time: " + str(self.start_time) + ">"

    __repr__ = __str__
