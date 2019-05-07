import numpy as np
from unittest import TestCase

from diffprivlib.mechanisms import Vector

func = lambda x: np.sum(x ** 2)


class TestVector(TestCase):
    def setup_method(self, method):
        self.mech = Vector()

    def teardown_method(self, method):
        del self.mech

    def test_not_none(self):
        self.assertIsNotNone(self.mech)

    def test_class(self):
        from diffprivlib.mechanisms import DPMechanism
        self.assertTrue(issubclass(Vector, DPMechanism))

    def test_no_params(self):
        with self.assertRaises(ValueError):
            self.mech.randomise(func)

    def test_no_epsilon(self):
        self.mech.set_dimensions(3, 10).set_sensitivity(1)
        with self.assertRaises(ValueError):
            self.mech.randomise(func)

    def test_neg_epsilon(self):
        self.mech.set_dimensions(3, 10).set_sensitivity(1)
        with self.assertRaises(ValueError):
            self.mech.set_epsilon(-1)

    def test_inf_epsilon(self):
        self.mech.set_dimensions(3, 10).set_sensitivity(1).set_epsilon(float("inf"))

        for i in range(100):
            noisy_func = self.mech.randomise(func)
            self.assertAlmostEqual(noisy_func(np.zeros(3)), 0)
            self.assertAlmostEqual(noisy_func(np.ones(3)), 3)

    def test_no_sensitivity(self):
        self.mech.set_dimensions(3, 10).set_epsilon(1)
        with self.assertRaises(ValueError):
            self.mech.randomise(func)

    def test_numeric_input(self):
        self.mech.set_dimensions(3, 10).set_epsilon(1).set_sensitivity(1)

        with self.assertRaises(TypeError):
            self.mech.randomise(1)

    def test_string_input(self):
        self.mech.set_dimensions(3, 10).set_epsilon(1).set_sensitivity(1)

        with self.assertRaises(TypeError):
            self.mech.randomise("1")

    def test_different_result(self):
        self.mech.set_dimensions(3, 10).set_epsilon(1).set_sensitivity(1)
        noisy_func = self.mech.randomise(func)

        for i in range(10):
            old_noisy_func = noisy_func
            noisy_func = self.mech.randomise(func)

            self.assertNotAlmostEqual(noisy_func(np.ones(3)), 3)
            self.assertNotAlmostEqual(noisy_func(np.ones(3)), old_noisy_func(np.ones(3)))
            # print(noisy_func(np.ones(3)))