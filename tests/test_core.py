import math
import unittest

from average_slope import average_slope


class AverageSlopeTests(unittest.TestCase):
    def test_irregular_sampling_uses_unweighted_mean(self):
        result = average_slope([0, 0.5, 1.5, 3, 5], [0, 2, 6, 9, 7])
        self.assertEqual(result.tmax, 3)
        self.assertEqual(result.cmax, 9)
        self.assertEqual(result.n_points, 4)
        self.assertEqual(result.interval_slopes, (4.0, 4.0, 2.0))
        self.assertTrue(math.isclose(result.average_slope, 10 / 3))

    def test_equally_spaced_case_equals_cmax_over_tmax(self):
        result = average_slope([0, 1, 2, 3, 4], [0, 3, 5, 6, 4])
        self.assertEqual(result.average_slope, result.cmax / result.tmax)
        self.assertEqual(result.average_slope, 2.0)

    def test_only_observations_through_tmax_are_used(self):
        result = average_slope([0, 1, 2, 3], [0, 4, 3, 1])
        self.assertEqual(result.interval_slopes, (4.0,))
        self.assertEqual(result.average_slope, 4.0)

    def test_tied_cmax_defaults_to_first_and_can_select_last(self):
        first = average_slope([0, 1, 2, 3], [0, 5, 5, 2])
        last = average_slope([0, 1, 2, 3], [0, 5, 5, 2], tmax_tie="last")
        self.assertEqual(first.tmax, 1)
        self.assertEqual(first.average_slope, 5)
        self.assertEqual(last.tmax, 2)
        self.assertEqual(last.average_slope, 2.5)

    def test_invalid_inputs(self):
        cases = [
        ([1, 2], [0, 1], "t=0"),
        ([0, 1, 1], [0, 1, 2], "strictly increasing"),
        ([0, 1], [0, -1], "non-negative"),
        ([0], [0], "at least two"),
        ([0, 1], [0], "same length"),
        ]
        for times, concentrations, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    average_slope(times, concentrations)

    def test_tmax_at_zero_is_not_computable(self):
        with self.assertRaisesRegex(ValueError, "Tmax is t=0"):
            average_slope([0, 1, 2], [4, 3, 2])


if __name__ == "__main__":
    unittest.main()
