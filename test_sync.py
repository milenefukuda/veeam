import unittest
from sync import hash_file
from sync import check_replica_folder
from unittest.mock import patch, mock_open

class TestHashFile(unittest.TestCase):

    def test_hash_file(self):
        temp_file_content  = b'test veeam content'
        test_file_path = "path/to/open"
       
        with patch("sync.open", mock_open(read_data=temp_file_content)) as mock_file:
            calculated_hash = hash_file(test_file_path)
            print(calculated_hash)

            expected_hash = '8d4718497ac6a3ab25a81238bfdc024b'

            self.assertEqual(calculated_hash, expected_hash)

class TestCheckReplicaFolder(unittest.TestCase):

    def test_check_replica_folder(self):
        test_source_folder = "random content"
        test_replica_folder = "random content"

        with patch("sync.open", mock_open(read_data=test_source_folder)) as mock_file:
            print("qqqq")
            check_replica_folder(test_source_folder,test_replica_folder)
            self.assertEqual(test_source_folder, test_replica_folder)

if __name__=='__main__':
    unittest.main()