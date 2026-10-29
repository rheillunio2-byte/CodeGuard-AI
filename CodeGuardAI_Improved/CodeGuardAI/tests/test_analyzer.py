import unittest
from analyzer import analyze_code

class AnalyzerTests(unittest.TestCase):
    def test_detects_eval(self):
        result = analyze_code("result = eval(user_input)", False, False)
        self.assertTrue(any(item["rule"] == "CG001" for item in result["findings"]))

    def test_empty_code(self):
        result = analyze_code("", False, False)
        self.assertEqual(result["findings"], [])

    def test_detects_hardcoded_secret(self):
        result = analyze_code('api_key = "abcde123456"', False, False)
        self.assertTrue(any(item["rule"] == "CG005" for item in result["findings"]))

if __name__ == "__main__":
    unittest.main()
