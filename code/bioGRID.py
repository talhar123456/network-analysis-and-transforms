from network import Network
from typing import Dict, List, Tuple, Union
from node import Node


class BioGRIDReader:
    def __init__(self, bioGRID_path: str):
        self.networks = {}

        with open('BIOGRID-ALL-4.4.232.tsv', 'r') as file:
            next(file)  # Skip header line
            for line in file:
                fields = line.strip().split('\t')
                taxon_id = fields[5]
                interactor_A = fields[7]
                interactor_B = fields[8]

                print(f"Taxon ID: {taxon_id}, Interactor A: {interactor_A}, Interactor B: {interactor_B}")

                # Skip self-interactions
                if interactor_A == interactor_B:
                    continue

                # Create network for taxon if not exists
                if taxon_id not in self.networks:
                    self.networks[taxon_id] = Network()

                network = self.networks[taxon_id]

                # Add interactors to the network if not already present
                if not network.has_node(interactor_A):
                    network.add_node(Node(interactor_A))
                if not network.has_node(interactor_B):
                    network.add_node(Node(interactor_B))

                # Add undirected edge between interactors
                network.add_edge(interactor_A, interactor_B)

        # Process and store the interaction and mapping data
        self.process_mapping_data()

    def organism_name(self, taxon_id: Union[int, str]) -> str:
        """
        Fetches the organism name associated with the given NCBI taxon ID. If the organism name is not in the mapping,
        this should return the taxon ID tagged with [name unknown], e.g. "1234 [name unknown]".

        :param taxon_id: NCBI taxon ID of an organism
        :return: the organism name associated with the taxon ID, or tagged taxon ID if the organism name is unknown
        :raises: KeyError (with a custom message) if the taxon ID is not included in the BioGRID data
        """
        return self.organism_mapping.get(str(taxon_id), f"{taxon_id} [name unknown]")

    def taxon_id(self, organism_name: str) -> str:
        """
        Fetches the NCBI taxon ID associated with the given organism name. This should be case agnostic, e.g.
        "Homo sapiens" and "homo sapiens" should both work. If the organism name is not in the mapping, this should
        return the organism name tagged with [ID unknown], e.g. "Homo sapiens [ID unknown]".

        :param organism_name: the scientific name of an organism, e.g. "Homo sapiens"
        :return: the NCBI taxon ID associated with the organism name
        """
        # Search for the organism name in the mapping, ignoring case
        for taxon_id, name in self.organism_mapping.items():
            if name.lower() == organism_name.lower():
                return str(taxon_id)
        return f"{organism_name} [ID unknown]"

    def network_size(self, taxon_id: Union[int, str]) -> int:
        """
        :param taxon_id: NCBI taxon ID of an organism
        :return: number of undirected interactions for the specified organism
        :raises: KeyError (with a custom message) if there is no data for an organism with that NCBI taxon ID
        """
        if str(taxon_id) not in self.networks:
            raise KeyError(f"No data available for organism with NCBI taxon ID {taxon_id}")
        return self.networks[str(taxon_id)].number_edges()
    
    def largest_networks(self, n: int) -> List[str]:
        """
        Returns the n organism taxon IDs with the most interactions.

        :param n: number of organisms
        :return: list of the n organisms with the most interactions
        """
        sorted_taxon_ids = sorted(self.networks.keys(), key=lambda x: self.network_size(x), reverse=True)
        return sorted_taxon_ids[:n]

    def most_abundant_taxon_ids(self, n: int) -> List[Tuple[int, str]]:
        """
        Compute the n organisms with the most interactions in BioGRID.

        :param n: number of organisms
        :return: list of the min(n, organisms in database) organisms with the most interactions and the respective
        number of interactions as (interactions, taxon IDs) pairs
        :raises: ValueError (with a custom message) if n is negative
        """
        # TODO
        raise NotImplementedError

    def highest_degree_interactors(self, taxon_id: Union[int, str], n: int) -> List[Tuple[int, str]]:
        """
        Compute the n interactors in the organism-specific network with the highest degree.

        :return: list of the min(n, interactors in the organism network) interactors with the highest degree in the
        organism-specific network as (degree, interactor symbol) pairs
        :raises: KeyError (with a custom message) if there is no data for an organism with that NCBI taxon ID
        :raises: ValueError (with a custom message) if n is negative
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if str(taxon_id) not in self.networks:
            raise KeyError(f"No data available for organism with NCBI taxon ID {taxon_id}")
        node_degrees = [(node.degree(), node.identifier) for node in self.networks[str(taxon_id)].nodes.values()]
        sorted_degrees = sorted(node_degrees, reverse=True)[:n]
        return sorted_degrees
    
    def export_network(self, taxon_id: Union[int, str], file_path: str, delimiter='\t'):
        """
        Writes the interactions of the specified organism into the specified file, matching the specifications of the
        export function in the Network-class.

        :param taxon_id: NCBI taxon ID of an organism
        :param file_path: path to the output network file
        :param delimiter: the delimiter that separates the two columns, default is a tab
        :raises: KeyError (with a custom message) if there is no data for an organism with that NCBI taxon ID
        """
        # TODO
        raise NotImplementedError

