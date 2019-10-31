import sys

class Node:
   def __init__(self, id):
      self.id = id
      self.neighbors = []
      self.routing_table = []
      self.table_updated = False

   def get_id(self):
      return self.id

   def set_neighbor(self, node, cost):
      self.neighbors.append(node)
      self.routing_table.append([node.get_id(), cost, node.get_id()])

   def print_rtable(self):
      #print(self.routing_table)
      print("Destination\tCost\tNext Hop")
      for entry in self.routing_table:
         print(f"{entry[0]}\t\t{entry[1]}\t{entry[2]}")

   def update_rtable(self):
      updated = False
      for entry in self.routing_table:
         if entry[0] != self.incoming_packet[0]:
            continue
         cost_to_neighbor = entry[1]

      for pair in self.incoming_packet[1]:
         if pair[0] == self.id:
            continue

         found = False
         for entry in self.routing_table:
            if entry[0] != pair[0]:
               continue
            found = True
            index = self.routing_table.index(entry)

         if found:
            if (pair[1] + cost_to_neighbor) < self.routing_table[index][1]:
               self.routing_table[index][1] = pair[1] + cost_to_neighbor
               self.routing_table[index][2] = self.incoming_packet[0]
         else:
            self.routing_table.append([pair[0], pair[1] + cost_to_neighbor, self.incoming_packet[0]])

   def receive_dv_packet(self, packet):
      self.incoming_packet = packet
      self.update_rtable()

   def generate_dv_packet(self):
      pairs = []
      for entry in self.routing_table:
         pairs.append([entry[0], entry[1]])
      return [self.id, pairs]

   def send_dv_packet(self):
      packet = self.generate_dv_packet()
      for node in self.neighbors:
         node.receive_dv_packet(packet)

def parse_file(file_name):
   topology = []
   with open(file_name, 'r') as input_file:
      for line in input_file:
         topology.append(line.split())
   return topology

def find_total_nodes(topology):
   nodes = []
   for line in topology:
      if line[0] not in nodes:
         nodes.append(line[0])
      if line[1] not in nodes:
         nodes.append(line[1])
   return len(nodes)

def set_neighbors(nodes, topology):
   for line in topology:
      nodes[int(line[0])].set_neighbor(nodes[int(line[1])], int(line[2]))
      nodes[int(line[1])].set_neighbor(nodes[int(line[0])], int(line[2]))

def main():
   file_name = sys.argv[1]
   num_rounds = int(sys.argv[2])
   topology = parse_file(file_name)
   number_of_nodes = find_total_nodes(topology)

   nodes = []
   for num in range(0, number_of_nodes):
      nodes.append(Node(num))

   set_neighbors(nodes, topology)

   for num in range(0, num_rounds):
      for node in nodes:
         node.send_dv_packet()

   for node in nodes:
      print(f"Node {nodes.index(node)} Routing Table:")
      node.print_rtable()
      print()

if __name__ == '__main__':
   main()
