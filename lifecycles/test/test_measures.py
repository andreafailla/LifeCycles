from unittest import TestCase

from lifecycles.measures import *


class MeasuresTest(TestCase):

    def test_normalized_shannon_entropy(self):
        with self.assertRaises(ZeroDivisionError):
            e = _normalized_shannon_entropy((1, 1), base=2)

        with self.assertRaises(ValueError):
            e = _normalized_shannon_entropy([], base=2)

        self.assertEqual(round(_normalized_shannon_entropy([2, 3, 2], base=2), 3), 0.918)

    def test_flow_entropy(self):
        self.assertEqual(facet_unicity((1, 1)), 0)
        self.assertEqual(facet_unicity(([])), 0)
        self.assertEqual(round(facet_unicity([2, 3, 2]), 3), 0.918)

    def test_contribution_factor(self):
        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = [{1, 2, 3}, {4, 5, 6, 7}]
        self.assertEqual(facet_identity(target_set, reference_set), 2 / 3)

        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = []
        self.assertEqual(facet_identity(target_set, reference_set), 0)

        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = [{1, 2, 3, 4, 5, 9}]
        self.assertEqual(facet_identity(target_set, reference_set), 1)

    def test_difference_factor(self):
        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = [{1, 2, 3}, {4, 5, 6, 7}]
        self.assertEqual(facet_outflow(target_set, reference_set), 1 / 6)

        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = []
        self.assertEqual(facet_outflow(target_set, reference_set), 1)

        target_set = {1, 2, 3, 4, 5, 9}
        reference_set = [{1, 2, 3, 4, 5, 9}]
        self.assertEqual(facet_outflow(target_set, reference_set), 0)
