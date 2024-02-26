from lifecycles import LifeCycle


def backward_event_names():
    return [
        "Birth",
        "Accumulation",
        "Growth",
        "Expansion",
        "Continue",
        "Merge",
        "Offspring",
        "Reorganization",
    ]


def forward_event_names():
    return [
        "Death",
        "Dispersion",
        "Shrink",
        "Reduction",
        "Continue",
        "Split",
        "Ancestor",
        "Disassemble",
    ]


def colormap():
    """
    return {
        "Birth": "tab:olive",
        "Accumulation": "tab:gray",
        "Growth": "tab:brown",
        "Expansion": "tab:purple",
        "Continue": "tab:pink",
        "Merge": "tab:red",
        "Offspring": "tab:blue",
        "Reorganization": "tab:orange",
        "Death": "tab:olive",
        "Dispersion": "tab:gray",
        "Shrink": "tab:brown",
        "Reduction": "tab:purple",
        "Split": "tab:red",
        "Ancestor": "tab:blue",
        "Disassemble": "tab:orange",
    }
    """
    return {
        "Birth": "tab:olive",
        "Accumulation": "#4CC89F",
        "Growth": "#929292",
        "Expansion": "#5C5C5C",
        "Continue": "#CFBAE1",
        "Merge": "#E34856",
        "Offspring": "#0DAAE9",
        "Reorganization": "tab:orange",
        "Death": "tab:olive",
        "Dispersion": "#4CC89F",
        "Shrink": "#929292",
        "Reduction": "#5C5C5C",
        "Split": "#E34856",
        "Ancestor": "#0DAAE9",
        "Disassemble": "tab:orange",
    }


def from_set_to_attribute_values(lc: LifeCycle, target: str, attr_name: str) -> list:
    """
    retrieve the list of attributes of the elements in a set

    :param lc: a LifeCycle object
    :param target: the id of the set
    :param attr_name: the name of the attribute
    :return: a list of attributes corresponding to the elements in the set
    """

    tid = int(target.split("_")[0])
    attributes = list()

    for elem in lc.get_group(target):
        attributes.append(lc.get_attributes(attr_name, of=elem)[tid])
    return attributes
