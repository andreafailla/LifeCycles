import pickle
import random
from collections import defaultdict
from unittest import TestCase

import lifecycles
from lifecycles import LifeCycle
from lifecycles.algorithms.measures import *


class MeasuresTest(TestCase):
    @staticmethod
    def lc4test():
        lc = LifeCycle(int)
        with open("testbed.pkl", "rb") as f:
            data = pickle.load(f)

        lc.add_partitions_from(data)

        attrs = defaultdict(dict)
        for tid in lc.temporal_ids():
            partition = lc.get_partition_at(tid)
            for set_id in partition:
                set_ = lc.get_group(set_id)
                for element in set_:
                    attrs[element][tid] = random.choice(["A", "B", "C", "D", "E"])
        lc.set_attributes(attrs, attr_name="attr")

        return lc

    def test_normalized_shannon_entropy(self):
        with self.assertRaises(ZeroDivisionError):
            e = _normalized_shannon_entropy((1, 1), base=2)

        with self.assertRaises(ValueError):
            e = _normalized_shannon_entropy([], base=2)

        self.assertEqual(
            round(_normalized_shannon_entropy([2, 3, 2], base=2), 3), 0.918
        )

    def test_facets(self):

        self.assertEqual(
            round(facet_metadata([1, 1, 1], [[1, 1, 1], [1, 1, 1]], base=2), 3),
            0.0,
        )

        self.assertEqual(
            round(facet_metadata([1, 2, 3], [[1, 1, 1], [1, 1, 1]], base=2), 3),
            1.0,
        )

        self.assertEqual(facet_unicity([1, 1, 1, 2, 2, 2]), 0)
        self.assertEqual(round(facet_unicity([1, 1, 1, 2, 2]), 1), 0.2)

        self.assertEqual(facet_identity({1, 2}, [{1}, {2}]), 1)
        self.assertEqual(facet_identity({1, 2}, [{1}, {2, 3}]), 0.75)

        self.assertEqual(facet_outflow({1, 3}, [{1}, {2}]), 0.5)
        self.assertEqual(facet_outflow({1, 2}, [{1}, {2}]), 0)

    def test_stability(self):
        lc = self.lc4test()
        self.assertEqual(
            round(stability(lc, "+"), 3),
            0.1,
        )

    def test_purity(self):
        self.assertEqual(purity([1, 1, 1, 2, 2]), (1, 0.6))

    def test_event_typicality(self):

        lc = self.lc4test()

        ws = lifecycles.event_weights(lc, "2_0", direction="+")
        self.assertEqual(event_typicality(ws), ("Death", 0.5784791965566715))
