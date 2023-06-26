import json
from collections import defaultdict


class LifeCycle(object):
    """
    A class to represent and analyze temporally-evolving sets.

    """

    def __init__(self, dtype: type = int) -> None:

        self.dtype = dtype
        self.to_int_mapping = dict() if dtype != int else None

        self.tids = []
        self.named_sets = defaultdict(set)
        self.tid_to_named_sets = defaultdict(list)
        self.attributes = defaultdict(dict)

    ############################## Convencience get methods ##########################################
    def temporal_ids(self) -> list:
        """
        retrieve the temporal ids of the dynaset

        :return: a list of temporal ids
        """
        return self.tids

    def universe_set(self) -> set:
        """
        retrieve the universe set

        :return: the universe set
        """
        universe = set()
        for set_ in self.named_sets.values():
            universe = universe.union(set_)
        return universe

    ############################## Partition methods ##########################################
    def add_partition(self, partition: list) -> None:
        """
        add a partition to the LifeCycle. A partition is a list of sets observed at a given time instant. Each
        partition will be assigned a unique id (tid) corresponding to the observation time, and each set in the
        partition will be assigned a unique name

        :param partition: a collection of sets
        :return
        """
        tid = len(self.tids)
        self.tids.append(tid)

        for i, group in enumerate(partition):
            name = str(tid) + '_' + str(i)
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

        :param partitions:
        :return:
        """
        for p in partitions:
            self.add_partition(p)

    def get_partition_at(self, tid: int) -> list:
        """
        retrieve a partition by id

        :param tid: the id of the partition to retrieve
        :return: the partition corresponding to the given id
        """
        return self.tid_to_named_sets[str(tid)]

    ############################## Attribute methods ##########################################
    def set_attributes(self, attributes: dict, attr_name: str) -> None:
        """
        set the temporal attributes of the elements in the LifeCycle
        The temporal attributes must be provided as a dictionary keyed by the element id and valued by a dictionary
        keyed by the temporal id and valued by the attribute value.

        :param attr_name: the name of the attribute
        :param attributes: a dictionary of temporal attributes
        :return:
        """
        self.attributes[attr_name] = attributes

    def get_attributes(self, attr_name, of=None) -> dict:
        """
        retrieve the temporal attributes of the LifeCycle

        :param attr_name: the name of the attribute
        :param of: the element for which to retrieve the attributes. If None, all attributes are returned
        :return: a dictionary keyed by element id and valued by a dictionary keyed by temporal id and valued by the
        attribute value
        """
        if of is None:
            return self.attributes[attr_name]
        else:
            return self.attributes[attr_name][of]

    ############################## Set methods ##########################################
    def get_set(self, name: str) -> set:
        """
        retrieve a set by name

        :param name: the name of the set to retrieve
        :return: the set corresponding to the given name
        """
        return self.named_sets[name]

    ############################## Element-centric methods ##########################################
    def get_element_membership(self, element: object) -> list:
        """
        retrieve the list of sets that contain a given element
        :param element: the element for which to retrieve the memberships
        :return: a list of set names that contain the given element
        """

        memberships = list()
        for name, set_ in self.named_sets.items():
            if element in set_:
                memberships.append(name)
        return memberships

    def get_all_element_memberships(self) -> dict:
        """
        retrieve the list of sets that contain each element in the LifeCycle
        :return:
        """

        memberships = defaultdict(list)

        for element in self.universe_set():
            for name, set_ in self.named_sets.items():
                if element in set_:
                    memberships[element].append(name)

        return memberships

    ############################## Flow methods ##########################################
    def get_set_flow(self, target: str, direction: str, min_branch_size: int = 1) -> dict:
        """
        compute the flow of a set w.r.t. a given temporal direction. The flow of a set is the collection of sets that
        contain at least one element of the target set, Returns a dictionary keyed by set name and valued by the
        intersection of the target set and the set corresponding to the key.

        :param target: the name of the set to analyze
        :param direction: the temporal direction in which the set is to be analyzed
        :param min_branch_size: the minimum size of the intersection between the target set and the set corresponding
        :return: a dictionary keyed by set name and valued by the intersection of the target set and the set
        """
        flow = dict()
        tid = int(target.split('_')[0])
        if direction == '+':
            ref_tid = tid + 1
        elif direction == '-':
            ref_tid = tid - 1
        else:
            raise ValueError("direction must either be + or -")
        reference = self.get_partition_at(ref_tid)
        target_set = self.get_set(target)

        for name in reference:
            set_ = self.get_set(name)
            branch = target_set.intersection(set_)
            if len(branch) >= min_branch_size:
                flow[name] = branch
        return flow

    def all_flows(self, direction: str, min_branch_size: int = 1) -> dict:
        """
        compute the flow of all sets w.r.t. a given temporal direction
        :param direction: the temporal direction in which the sets are to be analyzed
        :param min_branch_size: the minimum size of a branch to be considered
        :return:
        """
        all_flows = dict()
        for name in self.named_sets:
            all_flows[name] = self.get_set_flow(name, direction, min_branch_size=min_branch_size)

        return all_flows

    ############################## IO & conversion methods ##########################################
    def write_json(self, path: str) -> None:
        """
        save the LifeCycle to a json file

        :param path: the path to the json file
        :return:
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
        load the LifeCycle from a json file

        :param path: the path to the json file
        :return:
        """

        known_types = {
            'int': int,
            'float': float,
            'str': str,
            'bool': bool,
            'list': list,
            'set': set,
            'dict': dict
        }

        with open(path, "rt") as f:
            ds = json.loads(f.read())

        self.dtype = known_types[ds['dtype']]
        for name, set_ in ds['named_sets'].items():
            self.named_sets[name] = set(set_)
            self.tid_to_named_sets[int(name.split('_')[0])] = name

        self.to_int_mapping = {int(k): v for k, v in ds['mapping'].items()}
        self.tids = [int(i) for i in self.tid_to_named_sets.keys()]
        self.named_sets = {k: set(v) for k, v in ds['named_sets'].items()}
        self.to_int_mapping = {int(k): v for k, v in ds['mapping'].items()}


    def to_dict(self) -> dict:
        """
        convert the LifeCycle to a dictionary

        :return: a dictionary representation of the LifeCycle
        """
        return self.__dict__()

    def __dict__(self):

        return {
            'dtype': str(self.dtype).split("'")[1],
            'named_sets': self.named_sets,
            'mapping': self.to_int_mapping
        }

    def __eq__(self, other):
        return self.__dict__() == other.__dict__()
