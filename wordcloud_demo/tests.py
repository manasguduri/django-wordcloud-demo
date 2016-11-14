import unittest
import templatetags.wordcloud as wordcloud
import random


class RemapTests(unittest.TestCase):

    def test_empty_returns_empty(self):
        res = wordcloud.remap([])
        self.assertEqual(list(res), [])

    def test_singleton(self):
        lo, hi = 10, 30

        res = wordcloud.remap([random.randint(-9999999, 999999)], lo, hi)
        self.assertEqual(list(res), [hi])

    def test_scaling_pair(self):
        tlo, thi = [10, 30]
        res = list(wordcloud.remap([1, 2], tlo, thi))
        self.assertEqual(res[0], tlo)
        self.assertEqual(res[1], thi)


if __name__ == '__main__':
    unittest.main()
