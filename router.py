class Router:
    ids = []

    def __init__(self, links):
        # IDs start from 1.
        self.address = len(ids) + 1
        ids.append(self.id)

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
