import pickle
import random
from collections import defaultdict
from unittest import TestCase

from lifecycles import LifeCycle


class DynasetTest(TestCase):
    """
    TODO: To be checked with other element's data types
    TODO: test minimum branch size
    """

    @staticmethod
    def get_data():
        with open("testbed.pkl", "rb") as f:
            data = pickle.load(f)

        return data

    @staticmethod
    def random_attributes(lc):
        attrs = defaultdict(dict)
        for tid in lc.temporal_ids():
            partition = lc.get_partition_at(tid)
            for set_id in partition:
                set_ = lc.get_set(set_id)
                for element in set_:
                    attrs[element][tid] = random.choice(['A', 'B', 'C', 'D', 'E'])
        return attrs

    def test_dynaset(self):
        partitions = self.get_data()
        lc = LifeCycle(int)
        lc.add_partition(partitions[0])

        self.assertEqual(lc.get_partition_at(0), ['0_0', '0_1', '0_2', '0_3', '0_4', '0_5', '0_6', '0_7'])
        self.assertEqual(lc.get_set('0_0'), {93, 116, 127, 156, 233, 312, 404, 405, 425, 432, 535, 562, 612, 618, 655,
                                             657, 828, 829, 872, 874, 875, 879, 891, 911, 912, 928, 960, 961, 972, 1173,
                                             1253, 1265, 1273, 1324, 1329, 1342, 1359, 1420, 1425, 1485, 1514, 1517,
                                             1521, 1522, 1529, 1567, 1581, 1716, 1728, 1732, 1739, 1742, 1769, 1771,
                                             1794, 1824, 1825, 1873, 1878, 1879, 1913, 1984, 1994})

        lc.add_partitions_from(partitions[1:])
        self.assertEqual(lc.temporal_ids(), [0, 1, 2, 3, 4])
        self.assertEqual(len(lc.universe_set()), 2052)

        self.assertEqual(len(lc.get_partition_at(0)), len(partitions[0]))

    def test_membership(self):
        partitions = self.get_data()
        lc = LifeCycle(int)
        lc.add_partitions_from(partitions)

        self.assertEqual(lc.get_element_membership(2), ['0_7', '1_7'])

        memberships = lc.get_all_element_memberships()

        self.assertListEqual(list(memberships.keys()), list(lc.universe_set()))
        for v in memberships.values():
            self.assertGreater(len(v), 0)

    def test_attributes(self):
        data = self.get_data()
        lc = LifeCycle(int)
        lc.add_partitions_from(data)

        attrs = self.random_attributes(lc)
        lc.set_attributes(attributes=attrs, attr_name='fakeattr')

        fakeattr = lc.get_attributes('fakeattr')

        self.assertEqual(len(fakeattr), len(lc.universe_set()))

        for element in fakeattr:
            self.assertEqual(len(fakeattr[element]), len(lc.get_element_membership(element)))

        self.assertDictEqual(attrs, fakeattr)

    def test_flow(self):
        data = self.get_data()
        lc = LifeCycle(int)
        lc.add_partitions_from(data)

        flow = lc.get_set_flow('0_0', '+')
        self.assertEqual(flow, {'1_0': {116, 127, 156, 233, 312, 404, 405, 425, 535, 562, 618, 879, 891, 911, 960, 1173,
                                        1253, 1265, 1324, 1342, 1359, 1420, 1425, 1485, 1514, 1517, 1521, 1522, 1581,
                                        1716, 1728, 1732, 1739, 1742, 1794, 1873, 1878, 1913, 1994}, '1_5': {1824}})

        flow = lc.get_set_flow('1_0', '-')
        self.assertEqual(flow,
                         {'0_0': {116, 127, 156, 233, 312, 404, 405, 425, 535, 562, 618, 879, 891, 911, 960, 1173,
                                  1253, 1265, 1324, 1342, 1359, 1420, 1425, 1485, 1514, 1517, 1521, 1522, 1581, 1716,
                                  1728, 1732, 1739, 1742, 1794, 1873, 1878, 1913, 1994}})

    def test_conversion(self):
        data = self.get_data()
        lc = LifeCycle(int)

        lc.add_partitions_from(data)

        self.assertEqual(sorted(list(lc.to_dict().keys())),
                         ["dtype", "mapping", "named_sets"])

        lc.write_json('test.json')

        lc2 = LifeCycle(int)
        lc2.read_json('test.json')

        self.assertEqual(lc, lc2)
