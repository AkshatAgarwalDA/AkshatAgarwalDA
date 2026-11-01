import unittest
from src.analyze_sip import future_value_sip, required_starting_sip

class SipModelTests(unittest.TestCase):
    def test_zero_return_no_step_up(self):
        self.assertAlmostEqual(future_value_sip(1000, 0, 1, 0), 12000, places=6)
    def test_step_up_increases_corpus(self):
        self.assertGreater(future_value_sip(1000, 10, 10, 10), future_value_sip(1000, 10, 10, 0))
    def test_required_sip_reaches_target(self):
        sip = required_starting_sip(1_000_000, 10, 10, 5)
        self.assertGreaterEqual(future_value_sip(sip, 10, 10, 5), 1_000_000)
        self.assertLess(future_value_sip(sip * 0.999, 10, 10, 5), 1_000_000)

if __name__ == "__main__":
    unittest.main()
