"""Testes das funções de specs de impressão (stdlib unittest)."""

import unittest

from print_specs import (
    BLEED,
    TRIM_6X9,
    full_wrap_size,
    gutter_for,
    spine_width,
)


class PrintSpecsTest(unittest.TestCase):
    def test_spine_width_white(self):
        self.assertAlmostEqual(spine_width(100, "white"), 0.2252, places=4)

    def test_spine_width_rejects_below_minimum(self):
        with self.assertRaises(ValueError):
            spine_width(10)

    def test_spine_width_rejects_unknown_paper(self):
        with self.assertRaises(ValueError):
            spine_width(100, "papiro")

    def test_full_wrap_size_6x9(self):
        spine = 0.2
        w, h = full_wrap_size(*TRIM_6X9, spine)
        self.assertAlmostEqual(w, 12 + spine + 2 * BLEED, places=4)
        self.assertAlmostEqual(h, 9 + 2 * BLEED, places=4)

    def test_gutter_tiers(self):
        self.assertEqual(gutter_for(120), 0.375)
        self.assertEqual(gutter_for(200), 0.5)
        self.assertEqual(gutter_for(400), 0.625)


if __name__ == "__main__":
    unittest.main()
