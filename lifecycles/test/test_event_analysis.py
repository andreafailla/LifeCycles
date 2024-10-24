import pickle
import random
from collections import defaultdict
from unittest import TestCase

from lifecycles import LifeCycle
from lifecycles.algorithms.event_analysis import *


class EventAnalysisTest(TestCase):
    """
    Todo: test the following functions:
    - events_asur
    - event_graph_greene

    """

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

    def test_analyze_flow(self):
        lc = self.lc4test()

        self.assertEqual(
            analyze_flow(lc, "0_0", "+"),
            {"I": 0.5222062004325884, "O": 0.36507936507936506, "U": 0.95, "size": 63},
        )

        self.assertListEqual(
            sorted(analyze_flow(lc, "0_0", "-", attr="attr").keys()),
            sorted(
                [
                    "I",
                    "O",
                    "U",
                    "attr_H",
                    "attr_H_change",
                    "attr_mca",
                    "attr_purity",
                    "size",
                ]
            ),
        )

        self.assertDictEqual(
            analyze_flow(lc, "0_0", "-"), {"U": 1, "I": 0, "O": 1.0, "size": 63}
        )

    def test_events(self):

        lc = self.lc4test()
        evs = events_all(lc, "+")["+"]
        self.assertEqual(sorted(lc.groups_ids())[:-8], sorted(list((evs.keys()))))

        evs = events_all(lc, "-")["-"]
        self.assertEqual(sorted(lc.groups_ids())[8:], sorted(list((evs.keys()))))

        ev = event(lc, "2_0")
        fut_e, fut_score = ev["+"]
        self.assertEqual(fut_e, "Death")
        self.assertEqual(fut_score, 0.5784791965566715)
        past_e, past_score = ev["-"]
        self.assertEqual(past_e, "Offspring")
        self.assertEqual(past_score, 0.5076551168412571)

        fcts = facets(lc, "2_0", "+")
        self.assertEqual(sorted(fcts.keys()), ["I", "O", "U", "size"])
