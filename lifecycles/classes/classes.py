import json
from collections import defaultdict

__all__ = ["LifeCycle"]


class LifeCycle(object):
    """
    A class to represent and analyze temporally-evolving groups.

    :param dtype: the datatype of the elements in the groups.
    Supported types are int, float, str, list, and dict.

    :return: a LifeCycle object

    :Example:
    >>> lc = LifeCycle(dtype=int) # accepts int elements
    >>> lc = LifeCycle(dtype=str) # accepts str elements
    """

    def __init__(self, dtype: type = int) -> None:

        self.dtype = dtype

        self.tids = []
        self.named_sets = defaultdict(set)
        self.tid_to_named_sets = defaultdict(list)
        self.attributes = defaultdict(dict)

    ############################## Convenience get methods ##########################################
    def temporal_ids(self) -> list:
        """
        retrieve the temporal ids of the LifeCycle.
        Temporal ids are integers that represent the observation time of a partition.

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([{"a", "b"}, {"c", "d"}]) # at time 0
        >>> lc.add_partition([{"a", "b"}, {"c"}]) # at time 1
        >>> lc.temporal_ids()
        [0, 1]
        """
        return self.tids

    def slice(self, start: int, end: int) -> object:
        """
        slice the LifeCycle to keep only a given interval

        :param start: the start of the interval
        :param end: the end of the interval
        :return: a new LifeCycle object

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([{5,7}, {6,8}])
        >>> lc.add_partition([{5,7}, {1,6,8}])
        >>> sliced = lc.slice(0, 1)

        """
        temp = LifeCycle(self.dtype)
        temp.tids = self.tids[start:end]
        temp.named_sets = {
            k: v
            for k, v in self.named_sets.items()
            if int(k.split("_")[0]) in temp.tids
        }
        temp.tid_to_named_sets = {
            k: v for k, v in self.tid_to_named_sets.items() if int(k) in temp.tids
        }
        temp_attrs = {}
        for attr_name, attr in self.attributes.items():
            temp_attrs[attr_name] = {k: v for k, v in attr.items() if k in temp.tids}
        temp.attributes = temp_attrs
        return temp

    def universe_set(self) -> set:
        """
        retrieve the universe set.
        The universe set is the union of all sets in the LifeCycle

        :return: the universe set

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]]) # at time 0
        >>> lc.add_partition([{5,7}, {6,8}]) # at time 1
        >>> lc.universe_set()
        {1, 2, 3, 4, 5, 6, 7, 8}
        """
        universe = set()
        for set_ in self.named_sets.values():
            universe = universe.union(set_)
        return universe

    def groups_ids(self) -> list:
        """
        retrieve the group ids of the lifecycle. Each id is of the form 'tid_gid' where tid is the temporal id and
        gid is the group id. The group id is a unique identifier of the group within the temporal id.

        :return: a list of ids of the temporal groups

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([{5,7}, {6,8}])
        >>> lc.groups_ids()
        ['0_0', '0_1', '1_0', '1_1']
        """
        return list(self.named_sets.keys())

    ############################## Partition methods ##########################################
    def add_partition(self, partition: list) -> None:
        """
        add a partition to the LifeCycle. A partition is a list of sets observed at a given time instant. Each
        partition will be assigned a unique id (tid) corresponding to the observation time, and each set in the
        partition will be assigned a unique name

        :param partition: a collection of sets
        :return: None

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([{5,7}, {6,8}])
        """

        tid = len(self.tids)
        self.tids.append(tid)

        for i, group in enumerate(partition):
            name = str(tid) + "_" + str(i)
            self.tid_to_named_sets[str(tid)].append(name)

            if self.dtype in [int, float, str]:
                try:
                    self.named_sets[name] = set(group)
                except TypeError:  # group is not iterable (only 1 elem)
                    tmp = set()
                    tmp.add(group)
                    self.named_sets[name] = tmp

            elif self.dtype == dict:
                for elem in group:
                    to_str = json.dumps(elem)
                    self.named_sets[name].add(to_str)

            elif self.dtype == list:
                for elem in group:
                    to_str = str(elem)
                    self.named_sets[name].add(to_str)
            else:
                raise NotImplementedError("dtype not supported")

    def add_partitions_from(self, partitions: list) -> None:
        """
        add multiple partitions to the LifeCycle.

        :param partitions: a list of partitions
        :return: None

        :Example:
        >>> lc = LifeCycle()
        >>> partitions = [
        >>>     [[1,2], [3,4,5]],
        >>>     [{5,7}, {6,8}]
        >>> ]
        >>> lc.add_partitions_from(partitions)
        """
        for p in partitions:
            self.add_partition(p)

    def get_partition_at(self, tid: int) -> list:
        """
        retrieve a partition by id

        :param tid: the id of the partition to retrieve
        :return: the partition corresponding to the given id

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([{5,7}, {6,8}, {9}])
        >>> lc.get_partition_at(0)
        ['0_0', '0_1']
        >>> lc.get_partition_at(1)
        ['1_0', '1_1', '1_2']
        """
        if str(tid) not in self.tid_to_named_sets:
            return []
        return self.tid_to_named_sets[str(tid)]

    ############################## Attribute methods ##########################################
    def set_attributes(self, attributes: dict, attr_name: str) -> None:
        """
        set the temporal attributes of the elements in the LifeCycle

        The temporal attributes must be provided as a dictionary keyed by the element id and valued by a dictionary
        keyed by the temporal id and valued by the attribute value.

        :param attr_name: the name of the attribute
        :param attributes: a dictionary of temporal attributes
        :return: None

        :Example:

        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> attributes = {
        >>>     1: c{0: 'red', 1: 'blue'}, # element 1 is red at time 0 and blue at time 1
        >>>     2: {0: 'green', 1: 'magenta'} # element 2 is green at time 0 and magenta at time 1
        >>> }
        >>> lc.set_attributes(attributes, attr_name="color")
        """
        self.attributes[attr_name] = attributes

    def get_attributes(self, attr_name, of=None) -> dict:
        """
        retrieve the temporal attributes of the LifeCycle

        :param attr_name: the name of the attribute
        :param of: the element for which to retrieve the attributes. If None, all attributes are returned

        :return: a dictionary keyed by element id and valued by a dictionary keyed by temporal id and valued by the attribute value


        :Example:

        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> attributes = {
        >>>     1: {0: 'red', 1: 'blue'}, # element 1 is red at time 0 and blue at time 1
        >>>     2: {0: 'green', 1: 'magenta'} # element 2 is green at time 0 and magenta at time 1
        >>> }
        >>> lc.set_attributes(attributes, attr_name="color")
        >>> lc.get_attributes("color")
        >>> # {1: {0: 'red', 1: 'blue'}, 2: {0: 'green', 1: 'magenta'}}
        >>> lc.get_attributes("color", of=1) # get the attributes of element 1
        >>> # {0: 'red', 1: 'blue'}

        """
        if of is None:
            return self.attributes[attr_name]
        else:
            return self.attributes[attr_name][of]

    ############################## Set methods ##########################################
    def get_group(self, gid: str) -> set:
        """
        retrieve a group by id

        :param gid: the name of the group to retrieve
        :return: the group corresponding to the given name

        :Example:

        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.get_group("0_0")
        >>> # {1, 2}
        """
        return self.named_sets[gid]

    def group_iterator(self, tid: int = None) -> iter:
        """
        returns an iterator over the groups of the LifeCycle.
        if a temporal id is provided, it will iterate over the groups observed at that time instant

        :param tid: the temporal id of the groups to iterate over. Default is None
        :return: an iterator over the groups

        :Example:

        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> for set_ in lc.group_iterator():
        >>>     print(set_)
        >>> # {1, 2}
        >>> # {3, 4, 5}
        >>> # {1, 2, 3}
        >>> # {4, 5}

        """
        if tid is None:
            yield from self.named_sets.values()
        else:
            for name in self.get_partition_at(tid):
                yield self.named_sets[name]

    def filter_on_group_size(self, min_size: int = 1, max_size: int = None) -> None:
        """
        remove groups that do not meet the size criteria

        :param min_size: the minimum size of the groups to keep
        :param max_size: the maximum size of the groups to keep
        :return: None

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> lc.filter_on_group_size(min_size=3) # remove groups with less than 3 elements
        >>> lc.groups_ids() # only groups 1_0 and 1_1 remain
        >>> # ['0_1', '1_0']

        """

        if max_size is None:
            max_size = len(self.universe_set())

        for name, set_ in self.named_sets.copy().items():
            if len(set_) < min_size or len(set_) > max_size:
                del self.named_sets[name]
                self.tid_to_named_sets[name.split("_")[0]].remove(name)

    ############################## Element-centric methods ##########################################
    def get_element_membership(self, element: object) -> list:
        """
        retrieve the list of sets that contain a given element

        :param element: the element for which to retrieve the memberships
        :return: a list of set names that contain the given element

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> lc.get_element_membership(1)
        >>> # ['0_0', '1_0']

        """

        memberships = list()
        for name, set_ in self.named_sets.items():
            if element in set_:
                memberships.append(name)
        return memberships

    def get_all_element_memberships(self) -> dict:
        """
        retrieve the list of sets that contain each element in the LifeCycle

        :return: a dictionary keyed by element and valued by a list of set names that contain the element

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> lc.get_all_element_memberships()
        """

        memberships = defaultdict(list)

        for element in self.universe_set():
            for name, set_ in self.named_sets.items():
                if element in set_:
                    memberships[element].append(name)

        return memberships

    ############################## Flow methods ##########################################
    def group_flow(self, target: str, direction: str, min_branch_size: int = 1) -> dict:
        """
        compute the flow of a group w.r.t. a given temporal direction. The flow of a group is the collection of groups that
        contain at least one element of the target group, Returns a dictionary keyed by group name and valued by the
        intersection of the target group and the group corresponding to the key.

        :param target: the name of the group to analyze
        :param direction: the temporal direction in which the group is to be analyzed
        :param min_branch_size: the minimum size of the intersection between the target group and the group corresponding
        :return: a dictionary keyed by group name and valued by the intersection of the target group and the group

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> lc.group_flow("0_0", "+")
        >>> # {'1_0': {1, 2}}

        """
        flow = dict()
        tid = int(target.split("_")[0])
        if direction == "+":
            ref_tid = tid + 1
        elif direction == "-":
            ref_tid = tid - 1
        else:
            raise ValueError("direction must either be + or -")
        reference = self.get_partition_at(ref_tid)
        target_set = self.get_group(target)

        for name in reference:
            set_ = self.get_group(name)
            branch = target_set.intersection(set_)
            if len(branch) >= min_branch_size:
                flow[name] = branch
        return flow

    def all_flows(self, direction: str, min_branch_size: int = 1) -> dict:
        """
        compute the flow of all groups w.r.t. a given temporal direction

        :param direction: the temporal direction in which the sets are to be analyzed
        :param min_branch_size: the minimum size of a branch to be considered
        :return: a dictionary keyed by group name and valued by the flow of the group

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> lc.all_flows("+")
        >>> # {'0_0': {'1_0': {1, 2}}, '0_1': {'1_0': {3}, '1_1': {4, 5}}}

        """
        all_flows = dict()
        for name in self.named_sets:
            all_flows[name] = self.group_flow(
                name, direction, min_branch_size=min_branch_size
            )

        return all_flows

    ############################## IO & conversion methods ##########################################
    def write_json(self, path: str) -> None:
        """
        save the LifeCycle to a json file

        :param path: the path to the json file
        :return: None

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> lc.write_json("lc.json")

        """

        dic = dict()
        for k, v in self.to_dict().items():
            if isinstance(v, dict):
                v = {k_: list(v_) for k_, v_ in v.items()}
            dic[k] = v

        with open(path, "wt") as f:
            f.write(json.dumps(dic, indent=2))

    def read_json(self, path: str) -> None:
        """
        load the LifeCycle from a json file.
        If the dtype declared at instantiation differs from the one in the json file, the former will be overwritten by
        the latter.

        :param path: the path to the json file
        :return: None

        :Example:
        >>> lc = LifeCycle().read_json('lc.json')

        """

        known_types = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "set": set,
            "dict": dict,
        }

        with open(path, "rt") as f:
            ds = json.loads(f.read())

        self.dtype = known_types[ds["dtype"]]
        for name, set_ in ds["named_sets"].items():
            self.named_sets[name] = set(set_)
            self.tid_to_named_sets[int(name.split("_")[0])] = name

        self.tids = [int(i) for i in self.tid_to_named_sets.keys()]
        self.named_sets = {k: set(v) for k, v in ds["named_sets"].items()}
        print("Loaded LifeCycle from", path)

    def to_dict(self) -> dict:
        """
        convert the LifeCycle to a dictionary

        :return: a dictionary representation of the LifeCycle

        :Example:
        >>> lc = LifeCycle()
        >>> lc.add_partition([[1,2], [3,4,5]])
        >>> lc.add_partition([[1,2,3], [4,5]])
        >>> lc.to_dict()
        >>> # {'dtype': 'int', 'named_sets': {'0_0': {1, 2}, '0_1': {3, 4, 5}, '1_0': {1, 2, 3}, '1_1': {4, 5}}}

        """
        return self.__dict__()

    def __dict__(self):

        return {
            "dtype": str(self.dtype).split("'")[1],
            "named_sets": self.named_sets,
        }

    def __eq__(self, other):
        return self.__dict__() == other.__dict__()
