import unittest

from server.helpers.common_helper.hash_helper import get_list_hash


class TestHashHelper(unittest.TestCase):
    def test_get_hash_for_list_str(self) -> None:
        hash_0 = get_list_hash(["cat", "mouse"])
        hash_1 = get_list_hash(["cat", "mouse", "dog"])
        self.assertNotEqual(hash_0, hash_1)
