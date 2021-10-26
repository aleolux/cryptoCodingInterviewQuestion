import unittest

from main import get_price, import_data_to_list

CSV_FILE = "more_data.csv"
DATA = import_data_to_list(CSV_FILE)


class TestPrice(unittest.TestCase):
    def test_one_edge(self):
        result = get_price("BNB", "USDT", DATA)
        self.assertEqual(result, (280.0, ["BNB", "USDT"]))

    def test_one_two(self):
        result = get_price("DAI", "ETH", DATA)
        self.assertEqual(result, (1.0 / 2100, ["DAI", "ETH"]))

    def test_shortest_path_one(self):
        result = get_price("GBP", "EUR", DATA)
        self.assertEqual(result, (1.5, ["GBP", "USDT", "BTC", "EUR"]))

    def test_shortest_path_two(self):
        result = get_price("ETC", "EUR", DATA)
        self.assertEqual(result, (60, ["ETC", "BNB", "BTC", "EUR"]))

    def test_shortest_path_three(self):
        result = get_price("BTC", "GBP", DATA)
        self.assertEqual(result, (20000, ["BTC", "USDT", "GBP"]))

    def test_base_does_not_exist(self):
        result = get_price("XRP", "BTC", DATA)
        self.assertEqual(result, (0, []))

    def test_quote_not_linked(self):
        result = get_price("BTC", "ETH", DATA)
        self.assertEqual(result, (0, []))

    def test_quote_is_base(self):
        result = get_price("USDT", "USDT", DATA)
        self.assertEqual(result, (1, ["USDT"]))


if __name__ == '__main__':
    unittest.main()
