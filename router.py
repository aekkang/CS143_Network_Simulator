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
