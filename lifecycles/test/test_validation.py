from lifecycles.validation import all_validated_flows
from lifecycles.classes import LifeCycle
from unittest import TestCase
import pickle


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
        for direction in ['+', '-']:
            self.assertListEqual(
                list(all_validated_flows(lc, direction=direction).keys()),
                lc.set_ids()
            )
        self.assertListEqual(
            list(all_validated_flows(lc, direction='-').keys()),
            lc.set_ids()
        )
