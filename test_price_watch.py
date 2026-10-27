import unittest

from price_watch import decide, parse_price


class PriceWatchTest(unittest.TestCase):
    def test_parse_price_formats(self):
        pat = r'data-price="([\d\s.,]+)"'
        self.assertEqual(parse_price('<div data-price="1 299,90">', pat), 1299.9)
        self.assertEqual(parse_price('<div data-price="500">', pat), 500.0)
        self.assertIsNone(parse_price("<div>нет цены</div>", pat))

    def test_decide(self):
        self.assertEqual(decide(None, 100), "first")
        self.assertEqual(decide(100, 90), "drop")
        self.assertEqual(decide(100, 110), "rise")
        self.assertEqual(decide(100, 100), "same")


if __name__ == "__main__":
    unittest.main()
