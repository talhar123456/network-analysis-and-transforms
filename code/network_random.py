import random
from node import Node
from network import Network


class RandomNetwork(Network):
    """
    This network class implements a random, undirected network without self-edges. It inherits basic network
    functionality from the Network-class. You can add help functions to this class if you want.
    """
    def __init__(self, n_nodes=0, n_edges=0):
        """
        Creates a random network with the given number of nodes and edges.

        Suggested approach:
            1. create [n_nodes] nodes
            2. create [n_edges] edges between randomly selected nodes that are not yet connected

        Specification:
        - Edges are undirected and self-edges are not allowed.
        - Your code should not produce infinite loops.
        - Your code should not produce errors that are not specified in the doc string below.
        - In the end, the network must have the specified number of nodes and edges.

        :param n_nodes: the number of initial nodes (optional)
        :param n_edges: the number of initial edges (optional)
        :raises: ValueError (with custom message) if n_nodes or n_edges are negative
        :raises: ValueError (with custom message) if n_edges is larger than is possible for the given number of nodes
        """
        # make sure n_nodes or n_edges are not negative
        if n_nodes < 0:
            raise ValueError(f'The number of nodes ({n_nodes:,}) should not be negative.')
        if n_edges < 0:
            raise ValueError(f'The number of edges ({n_edges:,}) should not be negative.')

        # make sure that n_edges is not too large 
        max_undirected_edges = int((n_nodes * (n_nodes - 1)) / 2) if n_nodes else 0             

        if n_edges > max_undirected_edges:
            raise ValueError(f'The number of edges ({n_edges:,}) is higher than is possible ({max_undirected_edges:,}) '
                             f'for an undirected network with {n_nodes:,} nodes.')

        Network.__init__(self, undirected=True, allow_self_edges=False)

        if not n_nodes:
            return

        # create the specified number of nodes and add them to the network
        for i in range(n_nodes):
            self.add_node(Node(i))

        if not n_edges:
            return

        if n_edges == max_undirected_edges:
            for i in range(self.size()):
                for j in range(i + 1, self.size()):
                    self.add_edge(i, j)
            return

        established = 0                                         

        while established < n_edges:
            node_1, node_2 = random.sample(list(self.nodes.values()), 2)

            # if there already exists and edge between the two nodes, choose another pair of nodes
            if self.edge_exists(node_1, node_2):
                continue

            # add the edge
            self.add_edge(node_1, node_2)

            # increase the edge counter
            established += 1
