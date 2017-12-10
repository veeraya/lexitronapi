import unittest.mock

from api.lambda_handler import get_closest_search_terms


class TestLambdaHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_closest_search_terms_ends_with_s(self):
        closest_search_terms = get_closest_search_terms("friends")
        self.assertEqual(["friend"], closest_search_terms)

    def test_get_closest_search_terms_ends_with_es(self):
        closest_search_terms = get_closest_search_terms("pieces")
        self.assertEqual(["piece", "piec"], closest_search_terms)

    def test_get_closest_search_terms_ends_with_ies(self):
        closest_search_terms = get_closest_search_terms("enemies")
        self.assertEqual(["enemy", "enemie", "enemi"], closest_search_terms)

    def test_get_closest_search_terms_ends_with_ed(self):
        closest_search_terms = get_closest_search_terms("married")
        self.assertEqual(["marry", "marrie", "marri", "marr"], closest_search_terms)

    def test_get_closest_search_terms_ends_with_ss(self):
        closest_search_terms = get_closest_search_terms("tardiness")
        self.assertEqual([], closest_search_terms)

    def test_get_closest_search_terms_ends_with_ing(self):
        closest_search_terms = get_closest_search_terms("bribing")
        self.assertEqual(["bribe", "brib", "bri"], closest_search_terms)


if __name__ == '__main__':
    unittest.main()