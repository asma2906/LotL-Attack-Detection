
import unittest
import numpy as np

from src.models import build_short_model, build_long_model


class TestModelShapes(unittest.TestCase):

    def test_short_model_input_shape(self):
        model = build_short_model()
        self.assertEqual(model.input_shape, (None, 5, 6))

    def test_short_model_output_shape(self):
        model = build_short_model()
        self.assertEqual(model.output_shape, (None, 1))

    def test_long_model_input_shape(self):
        model = build_long_model()
        self.assertEqual(model.input_shape, (None, 20, 6))

    def test_long_model_output_shape(self):
        model = build_long_model()
        self.assertEqual(model.output_shape, (None, 1))

    def test_short_model_prediction_shape(self):
        model = build_short_model()
        sample = np.random.rand(2, 5, 6).astype("float32")
        prediction = model.predict(sample, verbose=0)
        self.assertEqual(prediction.shape, (2, 1))

    def test_long_model_prediction_shape(self):
        model = build_long_model()
        sample = np.random.rand(2, 20, 6).astype("float32")
        prediction = model.predict(sample, verbose=0)
        self.assertEqual(prediction.shape, (2, 1))


if __name__ == "__main__":
    unittest.main()
