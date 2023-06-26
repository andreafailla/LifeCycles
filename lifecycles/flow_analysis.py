from lifecycles.measures import *
from lifecycles.classes import LifeCycle

__all__ = ['analyze_all_flows', 'analyze_flow', "from_set_to_attribute_values", "event_weights"]


def from_set_to_attribute_values(lc: LifeCycle, set_name: str, attr_name: str) -> list:
    """
    retrieve the list of attributes of the elements in a set

    :param lc: a LifeCycle object
    :param set_name: the id of the set
    :param attr_name: the name of the attribute
    :return: a list of attributes corresponding to the elements in the set
    """

    tid = int(set_name.split('_')[0])
    attributes = list()

    for elem in lc.get_set(set_name):
        attributes.append(lc.get_attributes(attr_name, of=elem)[tid])
    return attributes


def _analyze_one_struct(target, reference) -> dict:
    # nb reference sets here are already filtered by minimum branch size

    ids_for_entropy = []
    # els_in_branches = set()
    for i, r in enumerate(reference):
        branch = target.intersection(r)
        ids_for_entropy.extend([str(i)] * len(branch))
        # els_in_branches.update(branch)
    # newels_ids = [str(j+len(reference)) for j in range(len(target.difference(els_in_branches)))]
    # ids_for_entropy.extend(newels_ids)

    return {'H': flow_entropy(ids_for_entropy),
            'W': contribution_factor(target, reference),
            'D': difference_factor(target, reference),
            'size': len(target)}


def _analyze_one_attr(target, reference, attr) -> dict:
    mca, pur = purity(target)
    try:
        ent = normalized_shannon_entropy(target, base=2)
    except ZeroDivisionError:
        ent = 0

    return {f'{attr}_H': ent,
            f'{attr}_H_change': attribute_entropy_change(target, reference, base=2),
            f'{attr}_purity': pur,
            f'{attr}_mca': mca
            }


def analyze_flow(lc: LifeCycle, target: str, direction: str, min_branch_size=1, attr: str = None) -> dict:
    """
    Analyze the flow of a set w.r.t. a given temporal direction.
    Specifically, compute the entropy of the flow, the contribution factor, the difference factor and the set size.
    If one of more attributes are specified via the attr parameter, also compute the entropy of the attribute values,
    the entropy change, the purity and the most common attribute value.
    In case min_branch_size is specified, all branches of the flow that include less than min_branch_size elements are
    discarded.
    :param lc:  a LifeCycle object
    :param target:  the name of the set to analyze
    :param direction:  the temporal direction in which the set is to be analyzed
    :param min_branch_size:  the minimum number of elements that a branch must contain to be considered
    :param attr:  the name or list of names of the attribute(s) to analyze. If None, no attribute is analyzed
    :return: a dictionary containing the analysis results
    """
    flow = lc.get_set_flow(target, direction=direction, min_branch_size=min_branch_size)

    reference_sets = [lc.get_set(name) for name in flow]
    analysis = _analyze_one_struct(lc.get_set(target), reference_sets)

    if attr is not None:
        attrs_to_analyze = [attr] if isinstance(attr, str) else attr
        for a in attrs_to_analyze:
            target_attrs = from_set_to_attribute_values(lc, target, a)
            reference_attrs = [from_set_to_attribute_values(lc, name, a) for name in flow]
            analysis.update(_analyze_one_attr(target_attrs, reference_attrs, a))
    return analysis


def analyze_all_flows(lc: LifeCycle, direction: str, min_branch_size: int = 1, attr=None) -> dict:
    """
    Analyze the flow of all sets in a LifeCycle object w.r.t. a given temporal direction.
    See analyze_flow for more details
    :param lc:
    :param direction:
    :param min_branch_size:
    :param attr:
    :return:
    """
    return {
        name: analyze_flow(lc, name, direction, min_branch_size=min_branch_size, attr=attr)
        for name in lc.named_sets
    }


def event_weights(analyzed_flows: dict, direction: str) -> dict:
    """
    Compute the event weights of the analyzed flows.

    :param analyzed_flows:  the result of the analysis of a flow
    :param direction:  the temporal direction in which the flow was analyzed
    :return: a dictionary containing the event weights
    """
    res = {}
    for id_, analyzed_flow in analyzed_flows.items():
        if direction == '-':
            res[id_] = {'is_birth': (1 - analyzed_flow['H']) * (1 - analyzed_flow['W']) * analyzed_flow['D'],
                        'is_congregation': analyzed_flow['H'] * (1 - analyzed_flow['W']) * analyzed_flow['D'],
                        'is_growth': (1 - analyzed_flow['H']) * analyzed_flow['W'] * analyzed_flow['D'],
                        'is_extension': analyzed_flow['H'] * analyzed_flow['W'] * analyzed_flow['D'],
                        'is_continue': (1 - analyzed_flow['H']) * analyzed_flow['W'] * (1 - analyzed_flow['D']),
                        'is_merge': analyzed_flow['H'] * analyzed_flow['W'] * (1 - analyzed_flow['D']),
                        'is_offspring': (1 - analyzed_flow['H']) * (1 - analyzed_flow['W']) * (1 - analyzed_flow['D']),
                        'is_reorganization': analyzed_flow['H'] * (1 - analyzed_flow['W']) * (1 - analyzed_flow['D'])
                        }
        elif direction == '+':
            res[id_] = {'is_death': (1 - analyzed_flow['H']) * (1 - analyzed_flow['W']) * analyzed_flow['D'],
                        'is_dispersion': analyzed_flow['H'] * (1 - analyzed_flow['W']) * analyzed_flow['D'],
                        'is_shrink': (1 - analyzed_flow['H']) * analyzed_flow['W'] * analyzed_flow['D'],
                        'is_reduction': analyzed_flow['H'] * analyzed_flow['W'] * analyzed_flow['D'],
                        'is_continue': (1 - analyzed_flow['H']) * analyzed_flow['W'] * (1 - analyzed_flow['D']),
                        'is_split': analyzed_flow['H'] * analyzed_flow['W'] * (1 - analyzed_flow['D']),
                        'is_ancestor': (1 - analyzed_flow['H']) * (1 - analyzed_flow['W']) * (1 - analyzed_flow['D']),
                        'is_disassemble': analyzed_flow['H'] * (1 - analyzed_flow['W']) * (1 - analyzed_flow['D'])
                        }
        else:
            raise ValueError(f"direction must be either '+' or '-'")

    return res
