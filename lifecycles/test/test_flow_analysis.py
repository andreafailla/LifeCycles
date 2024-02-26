import pickle
import random
from collections import defaultdict
from unittest import TestCase

from lifecycles import LifeCycle
from lifecycles.flow_analysis import *


class FlowAnalysisTest(TestCase):
    """
    TODO: Write tests for the following functions:
    - check against attributes
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
                    attrs[element][tid] = random.choice(['A', 'B', 'C', 'D', 'E'])
        lc.set_attributes(attrs, attr_name='attr')

        return lc

    def test_analyze_flow(self):
        lc = self.lc4test()

        self.assertEqual(analyze_flow(lc, '0_0', '+'),
                         {'D': 0.36507936507936506,
                          'H': 0.16866093149667025,
                          'W': 0.33155949233815135, 'size': 63})

        self.assertListEqual(sorted(analyze_flow(lc, '0_0', '-', attr='attr').keys()),
                             sorted(['D', 'H', 'W', 'attr_H', 'attr_H_change', 'size', 'attr_purity', 'attr_mca']))

        self.assertDictEqual(analyze_flow(lc, '0_0', '-'),
                             {'H': 0, 'W': 0.0, 'D': 1, 'size': 63})

    def test_analyze_all_flows(self):
        lc = self.lc4test()

        for op in ['+', '-']:
            self.assertListEqual(list(analyze_all_flows(lc, op).keys()), list(lc.named_sets.keys()))
