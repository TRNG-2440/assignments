"""
test_unit_converter.py

Test suite for the Unit Converter TDD activity.

These tests define the expected behaviour of a `unit_converter.py` module
that you must implement. Do not modify this file.

Run the suite at any time with:
    python -m unittest test_unit_converter.py -v

Your goal is to make every test pass without changing this file.
"""

import unittest
from unit_converter import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    celsius_to_kelvin,
    kelvin_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_to_fahrenheit,
    kilograms_to_pounds,
    pounds_to_kilograms,
    kilograms_to_ounces,
    ounces_to_kilograms,
    pounds_to_ounces,
    ounces_to_pounds,
    kilometers_to_miles,
    miles_to_kilometers,
    kilometers_to_feet,
    feet_to_kilometers,
    miles_to_feet,
    feet_to_miles,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def approx(a, b, tolerance=0.01):
    """Returns True if a and b are within tolerance of each other."""
    return abs(a - b) <= tolerance


# ---------------------------------------------------------------------------
# Temperature
# ---------------------------------------------------------------------------

class TestTemperatureConversions(unittest.TestCase):

    # --- Celsius to Fahrenheit ---

    def test_celsius_to_fahrenheit_boiling(self):
        self.assertTrue(approx(celsius_to_fahrenheit(100), 212.0))

    def test_celsius_to_fahrenheit_freezing(self):
        self.assertTrue(approx(celsius_to_fahrenheit(0), 32.0))

    def test_celsius_to_fahrenheit_body_temp(self):
        self.assertTrue(approx(celsius_to_fahrenheit(37), 98.6))

    def test_celsius_to_fahrenheit_negative(self):
        self.assertTrue(approx(celsius_to_fahrenheit(-40), -40.0))

    # --- Fahrenheit to Celsius ---

    def test_fahrenheit_to_celsius_boiling(self):
        self.assertTrue(approx(fahrenheit_to_celsius(212), 100.0))

    def test_fahrenheit_to_celsius_freezing(self):
        self.assertTrue(approx(fahrenheit_to_celsius(32), 0.0))

    def test_fahrenheit_to_celsius_negative(self):
        self.assertTrue(approx(fahrenheit_to_celsius(-40), -40.0))

    # --- Celsius to Kelvin ---

    def test_celsius_to_kelvin_freezing(self):
        self.assertTrue(approx(celsius_to_kelvin(0), 273.15))

    def test_celsius_to_kelvin_boiling(self):
        self.assertTrue(approx(celsius_to_kelvin(100), 373.15))

    def test_celsius_to_kelvin_absolute_zero(self):
        self.assertTrue(approx(celsius_to_kelvin(-273.15), 0.0))

    # --- Kelvin to Celsius ---

    def test_kelvin_to_celsius_absolute_zero(self):
        self.assertTrue(approx(kelvin_to_celsius(0), -273.15))

    def test_kelvin_to_celsius_freezing(self):
        self.assertTrue(approx(kelvin_to_celsius(273.15), 0.0))

    def test_kelvin_to_celsius_boiling(self):
        self.assertTrue(approx(kelvin_to_celsius(373.15), 100.0))

    # --- Fahrenheit to Kelvin ---

    def test_fahrenheit_to_kelvin_freezing(self):
        self.assertTrue(approx(fahrenheit_to_kelvin(32), 273.15))

    def test_fahrenheit_to_kelvin_boiling(self):
        self.assertTrue(approx(fahrenheit_to_kelvin(212), 373.15))

    # --- Kelvin to Fahrenheit ---

    def test_kelvin_to_fahrenheit_freezing(self):
        self.assertTrue(approx(kelvin_to_fahrenheit(273.15), 32.0))

    def test_kelvin_to_fahrenheit_boiling(self):
        self.assertTrue(approx(kelvin_to_fahrenheit(373.15), 212.0))


# ---------------------------------------------------------------------------
# Weight
# ---------------------------------------------------------------------------

class TestWeightConversions(unittest.TestCase):

    # --- Kilograms to Pounds ---

    def test_kilograms_to_pounds_one_kg(self):
        self.assertTrue(approx(kilograms_to_pounds(1), 2.2046))

    def test_kilograms_to_pounds_zero(self):
        self.assertTrue(approx(kilograms_to_pounds(0), 0.0))

    def test_kilograms_to_pounds_large(self):
        self.assertTrue(approx(kilograms_to_pounds(100), 220.46))

    # --- Pounds to Kilograms ---

    def test_pounds_to_kilograms_one_lb(self):
        self.assertTrue(approx(pounds_to_kilograms(1), 0.4536))

    def test_pounds_to_kilograms_zero(self):
        self.assertTrue(approx(pounds_to_kilograms(0), 0.0))

    def test_pounds_to_kilograms_large(self):
        self.assertTrue(approx(pounds_to_kilograms(200), 90.72))

    # --- Kilograms to Ounces ---

    def test_kilograms_to_ounces_one_kg(self):
        self.assertTrue(approx(kilograms_to_ounces(1), 35.274))

    def test_kilograms_to_ounces_zero(self):
        self.assertTrue(approx(kilograms_to_ounces(0), 0.0))

    # --- Ounces to Kilograms ---

    def test_ounces_to_kilograms_one_oz(self):
        self.assertTrue(approx(ounces_to_kilograms(1), 0.02835))

    def test_ounces_to_kilograms_sixteen_oz(self):
        self.assertTrue(approx(ounces_to_kilograms(16), 0.4536))

    # --- Pounds to Ounces ---

    def test_pounds_to_ounces_one_lb(self):
        self.assertTrue(approx(pounds_to_ounces(1), 16.0))

    def test_pounds_to_ounces_zero(self):
        self.assertTrue(approx(pounds_to_ounces(0), 0.0))

    def test_pounds_to_ounces_fraction(self):
        self.assertTrue(approx(pounds_to_ounces(0.5), 8.0))

    # --- Ounces to Pounds ---

    def test_ounces_to_pounds_sixteen_oz(self):
        self.assertTrue(approx(ounces_to_pounds(16), 1.0))

    def test_ounces_to_pounds_one_oz(self):
        self.assertTrue(approx(ounces_to_pounds(1), 0.0625))


# ---------------------------------------------------------------------------
# Distance
# ---------------------------------------------------------------------------

class TestDistanceConversions(unittest.TestCase):

    # --- Kilometers to Miles ---

    def test_kilometers_to_miles_one_km(self):
        self.assertTrue(approx(kilometers_to_miles(1), 0.6214))

    def test_kilometers_to_miles_zero(self):
        self.assertTrue(approx(kilometers_to_miles(0), 0.0))

    def test_kilometers_to_miles_marathon(self):
        self.assertTrue(approx(kilometers_to_miles(42.195), 26.219))

    # --- Miles to Kilometers ---

    def test_miles_to_kilometers_one_mile(self):
        self.assertTrue(approx(miles_to_kilometers(1), 1.6093))

    def test_miles_to_kilometers_zero(self):
        self.assertTrue(approx(miles_to_kilometers(0), 0.0))

    def test_miles_to_kilometers_marathon(self):
        self.assertTrue(approx(miles_to_kilometers(26.219), 42.195))

    # --- Kilometers to Feet ---

    def test_kilometers_to_feet_one_km(self):
        self.assertTrue(approx(kilometers_to_feet(1), 3280.84))

    def test_kilometers_to_feet_zero(self):
        self.assertTrue(approx(kilometers_to_feet(0), 0.0))

    # --- Feet to Kilometers ---

    def test_feet_to_kilometers_one_foot(self):
        self.assertTrue(approx(feet_to_kilometers(1), 0.000305))

    def test_feet_to_kilometers_five280_feet(self):
        # 5280 feet = 1 mile = 1.60934 km
        self.assertTrue(approx(feet_to_kilometers(5280), 1.6093))

    # --- Miles to Feet ---

    def test_miles_to_feet_one_mile(self):
        self.assertTrue(approx(miles_to_feet(1), 5280.0))

    def test_miles_to_feet_zero(self):
        self.assertTrue(approx(miles_to_feet(0), 0.0))

    def test_miles_to_feet_half_mile(self):
        self.assertTrue(approx(miles_to_feet(0.5), 2640.0))

    # --- Feet to Miles ---

    def test_feet_to_miles_5280_feet(self):
        self.assertTrue(approx(feet_to_miles(5280), 1.0))

    def test_feet_to_miles_one_foot(self):
        self.assertTrue(approx(feet_to_miles(1), 0.000189))


# ---------------------------------------------------------------------------
# Edge Cases and Error Handling
# ---------------------------------------------------------------------------

class TestEdgeCasesAndErrors(unittest.TestCase):

    # --- Below absolute zero ---

    def test_celsius_to_kelvin_below_absolute_zero_raises(self):
        with self.assertRaises(ValueError):
            celsius_to_kelvin(-274)

    def test_kelvin_to_celsius_below_absolute_zero_raises(self):
        with self.assertRaises(ValueError):
            kelvin_to_celsius(-1)

    def test_fahrenheit_to_kelvin_below_absolute_zero_raises(self):
        with self.assertRaises(ValueError):
            fahrenheit_to_kelvin(-460)

    # --- Negative weight ---

    def test_kilograms_to_pounds_negative_raises(self):
        with self.assertRaises(ValueError):
            kilograms_to_pounds(-1)

    def test_pounds_to_kilograms_negative_raises(self):
        with self.assertRaises(ValueError):
            pounds_to_kilograms(-5)

    def test_ounces_to_kilograms_negative_raises(self):
        with self.assertRaises(ValueError):
            ounces_to_kilograms(-0.5)

    # --- Negative distance ---

    def test_kilometers_to_miles_negative_raises(self):
        with self.assertRaises(ValueError):
            kilometers_to_miles(-1)

    def test_miles_to_kilometers_negative_raises(self):
        with self.assertRaises(ValueError):
            miles_to_kilometers(-10)

    def test_feet_to_kilometers_negative_raises(self):
        with self.assertRaises(ValueError):
            feet_to_kilometers(-100)

    # --- Type errors ---

    def test_celsius_to_fahrenheit_string_raises(self):
        with self.assertRaises(TypeError):
            celsius_to_fahrenheit("hot")

    def test_kilograms_to_pounds_string_raises(self):
        with self.assertRaises(TypeError):
            kilograms_to_pounds("heavy")

    def test_kilometers_to_miles_none_raises(self):
        with self.assertRaises(TypeError):
            kilometers_to_miles(None)

    # --- Floating point inputs ---

    def test_celsius_to_fahrenheit_float_input(self):
        self.assertTrue(approx(celsius_to_fahrenheit(36.6), 97.88))

    def test_kilograms_to_pounds_float_input(self):
        self.assertTrue(approx(kilograms_to_pounds(0.5), 1.1023))

    def test_kilometers_to_miles_float_input(self):
        self.assertTrue(approx(kilometers_to_miles(1.5), 0.9321))

