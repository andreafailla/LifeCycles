from unittest import TestCase

from lifecycles.measures import *


class MeasuresTest(TestCase):

    def test_normalized_shannon_entropy(self):
        with self.assertRaises(ZeroDivisionError):
            e = normalized_shannon_entropy((1, 1), base=2)

        with self.assertRaises(ValueError):
            e = normalized_shannon_entropy([], base=2)

        self.assertEqual(round(normalized_shannon_entropy([2, 3, 2], base=2), 3), 0.918)

    def test_flow_entropy(self):
        self.assertEqual(flow_entropy((1, 1)), 0)
        self.assertEqual(flow_entropy(([])), 0)
        self.assertEqual(round(flow_entropy([2, 3, 2]), 3), 0.918)

    def test_contribution_factor(self):
        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = [{1, 2, 3}, {4, 5, 6, 7}]
        self.assertEqual(contribution_factor(target_set, reference_set), 2 / 3)

        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = []
        self.assertEqual(contribution_factor(target_set, reference_set), 0)

        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = [{1, 2, 3, 4, 5, 9}]
        self.assertEqual(contribution_factor(target_set, reference_set), 1)

    def test_difference_factor(self):
        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = [{1, 2, 3}, {4, 5, 6, 7}]
        self.assertEqual(difference_factor(target_set, reference_set), 1 / 6)

        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = []
        self.assertEqual(difference_factor(target_set, reference_set), 1)

        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = [{1, 2, 3, 4, 5, 9}]
        self.assertEqual(difference_factor(target_set, reference_set), 0)
