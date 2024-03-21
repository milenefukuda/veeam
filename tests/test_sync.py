import unittest
import tempfile
import os
from sync import hash_file

class TestHashFile(unittest.TestCase):

    def test_hash_file(self):
        with tempfile.NamedTemporaryFile(delete=False, prefix='fev2') as test_file:
            test_file_path = test_file.name

        calculated_hash = hash_file(test_file_path)

        os.unlink(test_file_path)

        expected_hash = 'b3ecb989ed251cf95aba26793844e8a9'

        self.assertEqual(calculated_hash, expected_hash)

if __name__=='__main__':
    unittest.main()