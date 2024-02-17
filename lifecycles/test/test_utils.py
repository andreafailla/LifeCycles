from collections import defaultdict
from unittest import TestCase

from lifecycles.classes.classes import LifeCycle
from lifecycles.utils.utils import *


class UtilsTest(TestCase):
    def test_from_set_to_attribute_values(self):
        lc = LifeCycle(int)
        lc.add_partition([[1, 2, 3], [4, 5, 6], [7, 8]])
        attrs = defaultdict(dict)
        for tid in lc.temporal_ids():
            partition = lc.get_partition_at(tid)
            for set_id in partition:
                set_ = lc.get_set(set_id)
                for element in set_:
                    attrs[element][tid] = "VALUE"
        lc.set_attributes(attrs, attr_name="attr")
        res = get_set_attribute_values(lc, "0_0", "attr")
        self.assertListEqual(res, ["VALUE", "VALUE", "VALUE"])
