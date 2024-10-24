from itertools import combinations

__all__ = ["events_asur", "event_graph_greene"]


def _asur_merge_score(t: set, R: list) -> float:
    """
    Compute the asur merge score.

    defined as the ratio of the intersection of the target set and the union of the reference sets
    over the size of the largest set (either the target or the union of the reference sets)

    :param t: target set
    :param R: list of reference sets
    :return: merge score
    """
    union_reference = set.union(*R)
    res = len(union_reference.intersection(t)) / len(max([union_reference, t], key=len))
    return res


def _greene_merge_score(t: set, R: set) -> float:
    """
    Compute the greene merge score.
    based on the jaccard index

    :param t: target set
    :param R: reference set
    :return: merge score
    """

    return len(t.intersection(R)) / len(t.union(R))


def _find_asur_merge_events(lc: object, th: float) -> list:
    """
    Find merge events in a lifecycle according to Asur et al.

    :param lc: the lifecycle object
    :param th: cluster integrity threshold
    :return: dictionary of merge events
    """
    events = []
    for t in lc.temporal_ids()[1:]:  # start from the second time step
        for set_name in lc.get_partition_at(t):
            target = lc.get_group(set_name)
            flow = lc.group_flow(set_name, "-")
            r_names = list(flow.keys())  # names of the reference sets
            # compute for all pair of reference sets (combinations)
            for r1, r2 in combinations(r_names, 2):
                merge_score = _asur_merge_score(
                    target, [lc.get_group(r1), lc.get_group(r2)]
                )

                if merge_score > th:
                    events.append(
                        {
                            "src": set_name,
                            "type": "merge",
                            "score": merge_score,
                            "ref_sets": [r1, r2],  # names of the reference sets
                        }
                    )

    return events


def _find_asur_split_events(lc: object, th: float) -> list:
    """
    Find merge events in a lifecycle according to Asur et al.

    :param lc: the lifecycle object
    :param th: cluster integrity threshold
    :return: dictionary of merge events
    """
    events = []
    for t in lc.temporal_ids()[0:]:  # start from the second time step
        for set_name in lc.get_partition_at(t):
            target = lc.get_group(set_name)
            flow = lc.group_flow(set_name, "+")
            r_names = list(flow.keys())  # names of the reference sets
            # compute for all pair of reference sets (combinations)
            for r1, r2 in combinations(r_names, 2):
                merge_score = _asur_merge_score(
                    target, [lc.get_group(r1), lc.get_group(r2)]
                )

                if merge_score > th:
                    events.append(
                        {
                            "src": set_name,
                            "type": "split",
                            "score": merge_score,
                            "ref_sets": [r1, r2],  # names of the reference sets
                        }
                    )

    return events


def _find_asur_birth_events(lc: object) -> list:
    """
    Find continue events in a lifecycle according to Asur et al.

    :param lc: the lifecycle object
    :return: dictionary of continue events
    """
    events = []
    for t in lc.temporal_ids()[1:]:  # start from the second time step
        for set_name in lc.get_partition_at(t):
            flow = lc.group_flow(set_name, "-")
            r_names = list(flow.keys())  # names of the reference sets
            if len(r_names) == 0:
                events.append({"src": set_name, "type": "birth"})
    return events


def _find_asur_death_events(lc: object) -> list:
    """
    Find continue events in a lifecycle according to Asur et al.

    :param lc: the lifecycle object
    :return: dictionary of continue events
    """
    events = []
    for t in lc.temporal_ids()[0:-1]:  # start from the second time step
        for set_name in lc.get_partition_at(t):
            flow = lc.group_flow(set_name, "+")
            r_names = list(flow.keys())  # names of the reference sets
            if len(r_names) == 0:
                events.append({"src": set_name, "type": "death"})
    return events


def _find_asur_continue_events(lc: object) -> list:
    """
    Find continue events in a lifecycle according to Asur et al.

    :param lc: the lifecycle object
    :return: dictionary of continue events
    """
    events = []
    for t in lc.temporal_ids()[0:-1]:  # start from the second time step
        for set_name in lc.get_partition_at(t):
            flow = lc.group_flow(set_name, "+")
            r_names = list(flow.keys())  # names of the reference sets
            for name in r_names:
                if lc.get_group(name) == lc.get_group(set_name):
                    events.append(
                        {
                            "src": set_name,
                            "type": "continue",
                            "ref_set": name,
                        }
                    )
                    continue
    return events


def events_asur(lc: object, th: float = 0.5) -> dict:
    """
    Compute the events in a lifecycle according to Asur et al.
    Return a dictionary of events of the form {event_type: [event1, event2, ...]}

    :param lc: the lifecycle object
    :param th: threshold for merge and split scores. Defaults to 0.5.
    :return: dictionary of events

    :Reference:
        Asur, S., Parthasarathy, S., Ucar, D.: An event-based framework for charac-
        terizing the evolutionary behavior of interaction graphs. ACM Transactions on
        Knowledge Discovery from Data (TKDD) 3(4), 1–36 (2009)

    :Example:

    >>> from lifecycles import Lifecycle
    >>> from lifecycles.algorithms.classic_match import events_asur
    >>> lc = Lifecycle()
    >>> # add some data and then...
    >>> events = events_asur(lc, 0.5)
    """
    return {
        "merge": _find_asur_merge_events(lc, th),
        "split": _find_asur_split_events(lc, th),
        "birth": _find_asur_birth_events(lc),
        "death": _find_asur_death_events(lc),
        "continue": _find_asur_continue_events(lc),
    }


def event_graph_greene(lc: object, th: float = 0.1) -> list:
    """
    Compute the event graph in a lifecycle according to Greene et al.
    Return a list of match between groups, i.e., edges of the event graph.

    :param lc: the lifecycle object
    :param th: threshold for the Jaccard index. Defaults to 0.1 according to best results in the original paper.
    :return: list of match between groups

    :Reference:
        Greene, D., Doyle, D., Cunningham, P.: Tracking the evolution of communities in dynamic social networks. In: Proceedings of the 2010 International Conference on Advances in Social Networks Analysis and Mining (ASONAM 2010), pp. 176–183. IEEE (2010)


    :Example:

    >>> from lifecycles import Lifecycle
    >>> from lifecycles.algorithms.classic_match import event_graph_greene
    >>> lc = Lifecycle()
    >>> # add some data and then...
    >>> events = event_graph_greene(lc, 0.1)
    """
    events = []
    for t in lc.temporal_ids()[0:-1]:
        for set_name in lc.get_partition_at(t):
            target = lc.get_group(set_name)
            flow = lc.group_flow(set_name, "+")
            r_names = list(flow.keys())  # names of the reference sets
            # compute for all pair of reference sets (combinations)
            for r in r_names:
                merge_score = _greene_merge_score(target, lc.get_group(r))
                if merge_score > th:
                    events.append((t, set_name, r, merge_score))

    return events
