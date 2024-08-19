from node import Node
from network import Network


class FileNetwork(Network):
    """
    Creates a network from a network file, where each row consists of two columns, denoting two nodes that
    are connected by an edge.
    """
    def __init__(self, file_path: str, delimiter='\t', undirected=True, allow_self_edges=False):
        """
        Specification:
        - Skip rows with no, one, or more than 2 columns.
        - Do not produce errors when adding data to the network (e.g. adding an edge more than once).
        - It is fine if the network file is empty, the result is just an empty network.
        - If an unhandled error occurs while opening the file (e.g. the file does not exist), that is okay.

        :param file_path: path to the network file
        :param delimiter: symbol between columns in a row, default is a tab
        :param undirected: True if the network has undirected edges, False if the network is directed (optional)
        :param allow_self_edges: True if nodes are allowed to have edges to themselves, False otherwise (optional)
        """
        # initialise the Network class from which FileNetwork inherits its data structure and other functions
        # TODO: pass on the parameters
        Network.__init__(self, undirected=..., allow_self_edges=...)

        # TODO: open the network file and read it in its contents according to the parameters
        raise NotImplementedError

