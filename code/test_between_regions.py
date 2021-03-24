import unittest
import pandas as pd
from between_regions import between_region
from utils import connected


@unittest.skipIf(not connected(), "not connected to the internet")
class TestBetweenRegion(unittest.TestCase):
    def test_between_region(self):

        result_1 = between_region(["socks"],
                                  timeframe="2016-12-14 2017-01-25",
                                  geo="US",
                                  gprop="")
        result_2 = between_region(["socks", "shoes", "fish"],
                                  timeframe="2016-12-14 2017-01-25",
                                  geo="US",
                                  gprop="")

        expected_1 = pd.read_parquet("tests/test_data/between_region_1.parquet")
        expected_2 = pd.read_parquet("tests/test_data/between_region_2.parquet")

        self.assertTrue(expected_1.equals(result_1))
        self.assertTrue(expected_2.equals(result_2))