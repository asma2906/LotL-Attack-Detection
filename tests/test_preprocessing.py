import unittest


class TestPreprocessing(unittest.TestCase):

    def test_missing_values(self):
        values = ["PowerShell", None, "cmd.exe"]

        cleaned = [
            "missing" if value is None else str(value)
            for value in values
        ]

        self.assertEqual(cleaned, ["PowerShell", "missing", "cmd.exe"])

    def test_values_are_strings(self):
        values = [4688, 1, 0]

        cleaned = [str(value) for value in values]

        self.assertTrue(all(isinstance(value, str) for value in cleaned))


if __name__ == "__main__":
    unittest.main()
