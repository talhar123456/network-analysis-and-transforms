from bioGRID import BioGRIDReader
from network import Network
from network_scale_free import ScaleFreeNetwork
from tools import plot_distribution_comparison, scale_free_distribution, cumulative, KS_dist
from network_random import RandomNetwork
from tools import plot_distribution_comparison, scale_free_distribution



def exercise_1b():
    # Create scale-free networks
    n_nodes_1 = 10000
    n_nodes_2 = 100000
    m_edges = 2

    scale_free_net_1 = ScaleFreeNetwork(n_nodes=n_nodes_1, n_edges_per_iteration=m_edges)
    scale_free_net_2 = ScaleFreeNetwork(n_nodes=n_nodes_2, n_edges_per_iteration=m_edges)

    # compute degree distributions
    degree_distribution_1 = scale_free_net_1.degree_histogram()
    degree_distribution_2 = scale_free_net_2.degree_histogram()

    # plot degree distributions 
    plot_distribution_comparison(
        histograms=[degree_distribution_1, degree_distribution_2],
        legend=[f"n = {n_nodes_1}, m = {m_edges}", f"n = {n_nodes_2}, m = {m_edges}"],
        title="Degree Distribution of Scale-Free Networks",
        log=True
    )

    random_net = RandomNetwork(n_nodes=10000, n_edges=20000)

    # Compute degree distribution
    random_degree_distribution = random_net.degree_histogram()

    # Plot degree distributions
    plot_distribution_comparison(
        histograms=[degree_distribution_1, random_degree_distribution],
        legend=[f"Scale-Free (n = {n_nodes_1}, m = {m_edges})", f"Random (n = 10000, m = 20000)"],
        title="Degree Distribution Comparison",
        log=True
    )


def exercise_1c():
    # create a random network with n = 10,000 nodes and m = 20,000 edges
    random_net = RandomNetwork(n_nodes=10000, n_edges=20000)

    # degree distribution
    random_degree_distribution = random_net.degree_histogram()

    # theoretical power-law distribution
    max_degree = max(random_degree_distribution)
    gamma = 2.5  # Choose an appropriate value for gamma
    theoretical_distribution = scale_free_distribution(max_degree, gamma)

    # cumulative distributions
    random_cumulative_distribution = cumulative(random_degree_distribution)
    theoretical_cumulative_distribution = cumulative(theoretical_distribution)

    # Kolmogorov–Smirnov distance
    ks_distance = KS_dist(random_cumulative_distribution, theoretical_cumulative_distribution)

    print("Kolmogorov–Smirnov distance between random network degree distribution and theoretical power law distribution:", ks_distance)

    # plot the degree distribution & theoretical power law distribution
    plot_distribution_comparison(
        histograms=[random_degree_distribution, theoretical_distribution],
        legend=["Random Network", "Theoretical Power Law Distribution"],
        title="Degree Distribution Comparison",
        log=True
    )


def exercise_2b(bio_grid: BioGRIDReader):
    # TODO
    pass


def exercise_2c(bio_grid: BioGRIDReader):
    # filter interactions
    human_interactions = bio_grid.filter_human_interactions()

    # count unique interactions
    unique_interactions = len(set(human_interactions))

    print(f"The number of unique interactions in the human BioGRID network is: {unique_interactions}")

    # a Network object to represent the human interaction network
    human_network = Network()

    # add interactions
    for interaction in human_interactions:
        human_network.add_interaction(interaction)

    # get the 10 proteins 
    top_proteins = human_network.top_degree_proteins(10)

    # print the names and degrees of the top proteins
    print("Top 10 proteins with the highest degree in the human interaction network:")
    for protein, degree in top_proteins:
        print(f"Protein: {protein}, Degree: {degree}")

def plot_degree_distribution(network, log_scale=False):
    # compute degree distribution
    degree_distribution = network.degree_histogram()

    # compute normalized degree distribution
    max_degree = max(degree_distribution)
    normalized_distribution = [count / max_degree for count in degree_distribution]

    # plot distribution
    plt.plot(range(len(normalized_distribution)), normalized_distribution, marker='o', linestyle='-')
    plt.xlabel('Degree')
    plt.ylabel('Normalized Degree Distribution')
    if log_scale:
        plt.xscale('log')
        plt.yscale('log')
    plt.title('Normalized Degree Distribution')
    plt.show()


# main guard: this makes sure that the following is only executed when this file is called as a script directly
# that way, this file could be imported in other files to use the above functions without the processing below
# taking place every time
if __name__ == '__main__':
    print('# Exercise 1')
    exercise_1b()
    exercise_1c()

    # print('# Exercise 2')
    # read the BioGRID database here so that it only has to be done once
    bio_grid_reader = BioGRIDReader('BIOGRID-ALL-4.4.232.tsv')

    exercise_2b(bio_grid_reader)
    exercise_2c(bio_grid_reader)


