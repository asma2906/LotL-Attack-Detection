
import unittest
import pandas as pd

from src.preprocessing import (
    extract_event_techniques,
    prepare_event_data,
    create_labels,
    prepare_model_features,
    add_time_difference,
    split_by_agent,
)


class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            "_source.@timestamp": [
                "Jan 01, 2024 @ 00:00:02.000",
                "Jan 01, 2024 @ 00:00:01.000",
                "Jan 01, 2024 @ 00:00:03.000",
            ],
            "_source.agent.id": ["A", "A", "B"],
            "_source.data.win.system.eventID": [4688, 4689, 4688],
            "_source.data.win.eventdata.image": [
                "PowerShell.exe", None, "cmd.exe"
            ],
            "_source.data.win.eventdata.parentImage": [
                "explorer.exe", "cmd.exe", None
            ],
            "_source.data.win.eventdata.commandLine": [
                "powershell", None, "cmd"
            ],
            "_source.rule.mitre.id": ["T1059", "T1003", "T1059.001"],
            "_source.rule.mitre.technique": ["Test", "Test", "Test"],
            "_source.rule.mitre.tactic": ["Execution", "Credential Access", "Execution"],
        })

    def test_extract_event_techniques(self):
        result = extract_event_techniques("T1059 and T1059.001")

        self.assertEqual(result, {"T1059", "T1059.001"})

    def test_prepare_event_data_sorts_timestamps(self):
        result = prepare_event_data(self.data)

        self.assertTrue(
            result["_source.@timestamp"].is_monotonic_increasing
        )

    def test_create_labels(self):
        prepared = prepare_event_data(self.data)

        result = create_labels(prepared, {"T1059"})

        self.assertEqual(result["label"].tolist(), [0, 1, 1])

    def test_prepare_model_features(self):
        prepared = prepare_event_data(self.data)
        labelled = create_labels(prepared, {"T1059"})

        result = prepare_model_features(labelled)

        self.assertNotIn("_source.rule.mitre.id", result.columns)
        self.assertNotIn("_source.rule.mitre.technique", result.columns)
        self.assertNotIn("_source.rule.mitre.tactic", result.columns)

        self.assertEqual(
            result["_source.data.win.eventdata.image"].iloc[0],
            "missing"
        )

    def test_add_time_difference(self):
        prepared = prepare_event_data(self.data)
        labelled = create_labels(prepared, {"T1059"})
        features = prepare_model_features(labelled)

        result = add_time_difference(features)

        agent_a = result[result["_source.agent.id"] == "A"]

        self.assertEqual(agent_a["time_diff"].tolist(), [0.0, 1.0])

    def test_split_by_agent(self):
        rows = []

        for agent in ["A", "B"]:
            for i in range(10):
                rows.append({
                    "_source.agent.id": agent,
                    "_source.@timestamp": pd.Timestamp("2024-01-01")
                    + pd.Timedelta(seconds=i),
                    "label": i % 2
                })

        data = pd.DataFrame(rows)

        train, validation, test = split_by_agent(data)

        self.assertEqual(len(train), 14)
        self.assertEqual(len(validation), 2)
        self.assertEqual(len(test), 4)

        self.assertEqual(
            len(train) + len(validation) + len(test),
            len(data)
        )


if __name__ == "__main__":
    unittest.main()
