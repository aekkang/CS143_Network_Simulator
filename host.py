class Host:
    # List of existing addresses
    addresses = []

    def __init__(self, link):
        # Addresses start from 1.
        self.address = len(addresses) + 1
        addresses.append(self.address)

        # Each host is connected to a single link.
        self.link = link

    def send(self):
        '''
        Sends a packet.
        '''
        pass

    def generate(self):
        '''
        Makes a packet.
        '''
        pass

    # TODO: Do we need a receive function?
