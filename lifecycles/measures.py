from collections import Counter
from math import log, e

__all__ = [
    "entropy",
    "normalized_shannon_entropy",
    "flow_entropy",
    "contribution_factor",
    "difference_factor",
    "attribute_entropy_change",
    "purity"
]


def entropy(labels: list, base: int) -> float:
    """
    computes the Shannon entropy of a list of labels

    :param labels: the list of labels
    :param base: the base of the logarithm
    :return: the set entropy
    """
    n = len(labels)
    counter = Counter(labels)
    probabilities = [count / n for count in counter.values()]

    return -sum(p * log(p, base) for p in probabilities)


def normalized_shannon_entropy(labels, base=None):
    """
    the normalized Shannon entropy is the Shannon entropy divided by the maximum possible entropy
    (logb(n) where n is the number of labels)

    :param labels: the list of labels
    :param base: the base of the logarithm
    :return: the normalized Shannon entropy
    """

    base = e if base is None else base
    ent = entropy(labels, base)
    max_ent = log(len(list(set(labels))), base)

    normalized_entropy = ent / max_ent
    return normalized_entropy


def flow_entropy(labels: list) -> float:
    """
    the flow entropy quantifies the extent to which a target set comes from one (=0) or multiple (->1) flows.
    It is computed as the normalized Shannon entropy of the set labels of the nodes in the flow.
    As an example, if the target set receives three elements from set "3_2" and two elements from set "3_3",
    the flow entropy is the normalized Shannon entropy of the list ["3_2", "3_2", "3_2", "3_3", "3_3"].

    :param labels: the list of labels
    :return: the flow entropy
    """

    if len(set(labels)) < 2:
        return 0
    else:
        return normalized_shannon_entropy(labels)


def contribution_factor(target: set, reference: list):
    """
    the contribution factor is


    :param target: the target set
    :param reference: the reference sets
    :return: the contribution factor
    """
    w = 0
    for r in reference:
        flow = r.intersection(target)
        w += len(flow) * len(flow) / len(r)
    w = w / len(target)
    return w


def difference_factor(target: set, reference: list):
    """
    the difference factor is the ratio of the number of elements
    in the target set that are not in any of the reference sets

    :param target: the target set
    :param reference: the reference sets
    :return: the difference factor
    """
    try:
        return len(target.difference(set.union(*reference))) / len(target)
    except TypeError:  # if reference is empty
        return 1


def attribute_entropy_change(target_labels, reference_labels, base=None):
    """
    compute the change in attribute entropy between a target set and a reference set

    :param target_labels: the labels of the target set
    :param reference_labels: the labels of the reference sets
    :param base: the base of the logarithm
    :return: the change in attribute entropy
    """
    base = e if base is None else base
    try:
        target_entropy = normalized_shannon_entropy(target_labels, base)
    except ZeroDivisionError:
        target_entropy = 0

    reference_entropy = 0
    if len(reference_labels) > 0:
        for labels in reference_labels:
            try:
                reference_entropy += normalized_shannon_entropy(labels, base)
            except ZeroDivisionError:
                continue

        reference_entropy /= len(reference_labels)
    else:
        return None
    return target_entropy - reference_entropy


def purity(labels: list) -> tuple:
    """
    compute the purity of a set of labels. Purity is defined as the relative frequency of the most frequent attribute value

    :param labels:
    :param target_labels: the atttributes of the target set
    :return: a tuple of the most frequent attribute value and its frequency
    """
    mca, freq = Counter(labels).most_common(1)[0]
    return mca, freq / len(labels)


