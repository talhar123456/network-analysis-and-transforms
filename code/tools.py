import matplotlib.pyplot as plt
from typing import List, Union


def plot_distribution_comparison(histograms: List[List[float]], legend: List[str], title: str, log: bool):
    """
    Plots a list of histograms with matching list of descriptions as the legend with logarithmic axes.
    There is nothing to do here.

    :param histograms: list of histograms
    :param legend: list of matching histogram names
    :param title: plot title
    :param log: True if the plot axes should be in logarithmic scale, False otherwise
    :raises: ValueError (with custom message) if histograms or legend are empty
    :raises: ValueError (with custom message) if the number of histograms does not match the number of legend entries
    """
    # check the input
    if not histograms:
        raise ValueError('The list of histograms is empty.')
    if not legend:
        raise ValueError('The legend is empty.')
    if len(histograms) != len(legend):
        raise ValueError('The number of histograms does not match the number of legend entries.')

    # use subplot to make it easier to set the scale of the axes
    ax = plt.subplot()

    # set the axes to logarithmic scale if specified
    if log:
        ax.set_xscale('log')
        ax.set_yscale('log')

    # determine the length of the longest distribution
    longest = max(len(histogram) for histogram in histograms)               # type: int

    # extend "shorter" distributions
    for histogram in histograms:
        histogram.extend([0.0] * (longest - len(histogram)))

    # plots histograms
    for histogram in histograms:
        ax.plot(range(len(histogram)), histogram, marker='x', linestyle='' if log else '-')

    # axis labels
    plt.xlabel('degree k [log]' if log else 'degree k')
    plt.ylabel('probability of degree k (P(k)) [log]' if log else 'probability of degree k (P(k))')

    # finish the plot
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def scale_free_distribution(max_degree: int, gamma: float) -> List[float]:
    """
    Generates a power law distribution histogram up to the maximum degree with slope gamma. Make sure that both degree 0
    and max_degree are included in the distribution!

    :param max_degree: maximum degree to be included in the distribution
    :param gamma: slope of the power law distribution
    :return: normalized power law histogram
    :raises: ValueError (with a custom message) if the maximum degree is negative
    """
    if max_degree < 0:
        raise ValueError("Maximum degree should be non-negative.")

    histogram = [(k ** (-gamma)) for k in range(1, max_degree + 1)]

    # compute the normalization constant
    normalization_constant = sum(k * hk for k, hk in enumerate(histogram, start=1))

    # normalize the histogram
    normalized_histogram = [hk / normalization_constant for hk in histogram]

    # include degree 0
    normalized_histogram.insert(0, 0.0)

    return normalized_histogram


def cumulative(dist: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Computes the cumulative distribution of a probabilistic distribution.

    :param dist: probabilistic distribution
    :return: cumulative distribution
    """
    # initialize an empty list 
    cumulative_dist = []

    # initialize a variable 
    cumulative_sum = 0

    # iterate through the elements of the input distribution
    for value in dist:
        cumulative_sum += value

        # append the cumulative sum to the cumulative distribution list
        cumulative_dist.append(cumulative_sum)

    return cumulative_dist


def KS_dist(histogram_a: List[Union[int, float]], histogram_b: List[Union[int, float]]) -> float:
    """
    Computes the Kolmogorov-Smirnov distance between two histograms:
    1. Convert the histograms to cumulative distributions.
    2. Find the position where the cumulative distributions differ the most and return that difference.

    :param histogram_a: first histogram
    :param histogram_b: second histogram
    :raises: ValueError (with a custom message) if one or both of the histograms are empty
    :return: maximal distance
    """
    # check if histograms are empty
    if not histogram_a or not histogram_b:
        raise ValueError("Histograms cannot be empty.")

    # compute cumulative distributions
    cumulative_a = cumulative(histogram_a)
    cumulative_b = cumulative(histogram_b)

    # find the maximum absolute difference between cumulative distributions
    max_difference = max(abs(cumulative_a[i] - cumulative_b[i]) for i in range(min(len(cumulative_a), len(cumulative_b))))

    return max_difference