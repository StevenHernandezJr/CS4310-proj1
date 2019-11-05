import sys

class Node:
    # Initialize the node's id and two lists
    def __init__(self, id):
        self.id = id
        self.routing_table = []
        self.neighbor_links = []
        self.incoming_packet = None
        self.outgoing_packet = None

    def get_id(self):
        return self.id

    # Display formatted output representing the node's routing table
    def print_routing_table(self):
        print(f"Node {self.id} Routing Table:")
        print("Destination\tCost\tNext Hop")
        for entry in self.routing_table:
            print(f"{entry[0]}\t\t{entry[1]}\t{entry[2]}")
        print()

    # Add a "direct link" to a neighboring node and add it to the routing table
    def set_link(self, neighbor, cost):
        self.neighbor_links.append(neighbor)
        self.routing_table.append([neighbor.get_id(), cost, neighbor.get_id()])

    def prepare_dv_packet(self):
        pairs = []
        for entry in self.routing_table:
            pairs.append([entry[0], entry[1]])
        self.outgoing_packet = [self.id, pairs]

    # Generate DV packet and send it to each neighboring node
    def send_dv_packet(self):
        #pairs = []
        #for entry in self.routing_table:
        #    pairs.append([entry[0], entry[1]])
        #packet = [self.id, pairs]

        for link in self.neighbor_links:
            #link.set_dv_packet(packet)
            link.set_dv_packet(self.outgoing_packet)
        self.outgoing_packet = None

    # Save DV packet from neighbor
    def set_dv_packet(self, incoming_packet):
        self.incoming_packet = incoming_packet

    # Update routing table using DV packet if needed
    def update_routing_table(self):
        updated = False
        if self.incoming_packet == None:
            return updated

        for entry in self.routing_table:
            if self.incoming_packet[0] != entry[0]:
                continue
            cost_to_neighbor = entry[1]

        for pair in self.incoming_packet[1]:
            if pair[0] == self.id:
                continue

            new_cost = pair[1] + cost_to_neighbor
            found = False
            for entry in self.routing_table:
                if entry[0] != pair[0]:
                    continue
                found = True
                index = self.routing_table.index(entry)

            if found:
                if new_cost < self.routing_table[index][1]:
                    self.routing_table[index][1] = new_cost
                    self.routing_table[index][2] = self.incoming_packet[0]
                    updated = True
            else:
                self.routing_table.append([pair[0], new_cost, self.incoming_packet[0]])
                updated = True

        self.incoming_packet = None
        return updated

# Parse the topology file and return a list containing each line as an element
def parse_input_file(file_name):
    topology = []
    with open(file_name, 'r') as input_file:
        for line in input_file:
            topology.append(line.split())
    return topology

# Find total amount of nodes in network and return a list of Node objects
def count_nodes(topology):
    nodes = []
    for entry in topology:
        if entry[0] not in nodes:
            nodes.append(entry[0])
        if entry[1] not in nodes:
            nodes.append(entry[1])
    num_nodes = len(nodes)

    nodes.clear()

    for num in range(0, num_nodes):
        nodes.append(Node(num))
    return nodes

# Setup direct link according to each line in network topology
def setup_network_links(topology, nodes):
    for line in topology:
        nodes[int(line[0])].set_link(nodes[int(line[1])], int(line[2]))
        nodes[int(line[1])].set_link(nodes[int(line[0])], int(line[2]))

# Main function
def main():
    # Get name of topology file from command line argument
    # Get number of rounds to run simulator from command line argument
    file_name = sys.argv[1]
    num_rounds = int(sys.argv[2])

    # Parse the topology file to get network topology in the form of a list
    # Find total nodes in network and get a list containing each node
    # Assign links between nodes according to network topology
    network_topology = parse_input_file(file_name)
    node_list = count_nodes(network_topology)
    setup_network_links(network_topology, node_list)
    
    # Run simulator for given amount of rounds
    for num in range(0, num_rounds):
        #print(f"Round {num+1}:\n")
        for node in node_list:
            node.prepare_dv_packet()

        for node in node_list:
            node.send_dv_packet()
            for inner_node in node_list:
                if inner_node.update_routing_table():
                    #print(f"Node {node_list.index(inner_node)} routing table updated...")
                    pass
            
    for node in node_list:
        node.print_routing_table()

if __name__ == '__main__':
    main()