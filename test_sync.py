import unittest
import os
import shutil
import logging
from unittest.mock import patch, mock_open

from sync import hash_file
from sync import synchronize_folders

class TestSync(unittest.TestCase):

    def test_hash_file(self):
        temp_file_content  = b'test veeam content'
        test_file_path = "path/to/open"
       
        with patch("sync.open", mock_open(read_data=temp_file_content)) as mock_file:
            calculated_hash = hash_file(test_file_path)
            print(calculated_hash)

            expected_hash = '8d4718497ac6a3ab25a81238bfdc024b'

            self.assertEqual(calculated_hash, expected_hash)

    def test_synchronize_folders(self):
        logger = logging.getLogger(__name__)
        source_dir = "source_test"
        replica_dir = "replica_test"
        test_source_file = source_dir + "/veeamcontent.txt"
        test_replica_file = replica_dir + "/veeamcontent.txt"
        os.makedirs(source_dir)
        os.makedirs(replica_dir)

        with open(test_source_file, 'w') as fp:
            pass

        synchronize_folders(source_dir, replica_dir, logger)
        self.assertTrue(os.path.exists(test_replica_file))
        self.addCleanup(shutil.rmtree, source_dir)
        self.addCleanup(shutil.rmtree, replica_dir)

if __name__=='__main__':
    unittest.main()