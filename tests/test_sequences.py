
import unittest
import numpy as np
import pandas as pd


# Same function used in the notebook for the short-sequence model
def create_short_sequences(data, feature_cols, sequence_length=5):
    X = []
    y = []

    for agent_id, group in data.groupby("_source.agent.id"):
        group = group.sort_values("_source.@timestamp").reset_index(drop=True)

        features = group[feature_cols].values
        labels = group["label"].values

        for i in range(len(group) - sequence_length + 1):
            X.append(features[i:i + sequence_length])
            y.append(labels[i + sequence_length - 1])

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)


# Same function used in the notebook for the long-sequence model
def create_sequences(data, feature_cols, sequence_length=20):
    X = []
    y = []

    for agent_id, group in data.groupby("_source.agent.id"):
        group = group.sort_values("_source.@timestamp").reset_index(drop=True)

        features = group[feature_cols].values
        labels = group["label"].values

        for i in range(len(group) - sequence_length + 1):
            X.append(features[i:i + sequence_length])

            # Label of the final event in the sequence
            y.append(labels[i + sequence_length - 1])

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)


class TestSequenceCreation(unittest.TestCase):

    def setUp(self):
        self.short_data = pd.DataFrame({
            "_source.agent.id": ["A"] * 6,
            "_source.@timestamp": [1, 2, 3, 4, 5, 6],
            "feature": [10, 20, 30, 40, 50, 60],
            "label": [0, 0, 1, 0, 1, 1]
        })

        self.long_data = pd.DataFrame({
            "_source.agent.id": ["A"] * 20,
            "_source.@timestamp": list(range(1, 21)),
            "feature": list(range(10, 210, 10)),
            "label": [0] * 19 + [1]
        })

    def test_short_sequence_length(self):
        X, y = create_short_sequences(self.short_data, ["feature"])

        self.assertEqual(X.shape, (2, 5, 1))

    def test_long_sequence_length(self):
        X, y = create_sequences(self.long_data, ["feature"])

        self.assertEqual(X.shape, (1, 20, 1))

    def test_short_last_event_label(self):
        X, y = create_short_sequences(self.short_data, ["feature"])

        np.testing.assert_array_equal(y, [1, 1])

    def test_long_last_event_label(self):
        X, y = create_sequences(self.long_data, ["feature"])

        np.testing.assert_array_equal(y, [1])

    def test_output_data_types(self):
        X, y = create_short_sequences(self.short_data, ["feature"])

        self.assertEqual(X.dtype, np.float32)
        self.assertEqual(y.dtype, np.int32)


if __name__ == "__main__":
    unittest.main()
