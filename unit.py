import hashlib
import unittest
from sync import hash_file

def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Specify the path to your test file
test_file_path = "source/fev2.png"

# Calculate the MD5 hash of the test file
expected_hash = calculate_md5(test_file_path)

print("Expected MD5 hash:", expected_hash)

