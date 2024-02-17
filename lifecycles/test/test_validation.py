import pickle
from unittest import TestCase

from lifecycles.classes import LifeCycle
from lifecycles.validation import validate_all_flows


class ValidationTest(TestCase):
    @staticmethod
    def get_data():
        with open("testbed.pkl", "rb") as f:
            data = pickle.load(f)

        return data

    def test_validate_all_flows(self):
        data = self.get_data()
        lc = LifeCycle(int)
        lc.add_partitions_from(data)
        for direction in ["+", "-"]:
            self.assertListEqual(
                list(validate_all_flows(lc, direction=direction).keys()), lc.set_ids()
            )
        self.assertListEqual(
            list(validate_all_flows(lc, direction="-").keys()), lc.set_ids()
        )
