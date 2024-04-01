import os
import shutil
import hashlib
import time
import logging
import sys

def setup_logger(log_file):
    # Create logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=log_file, encoding="utf-8", level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    # # Create console handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # # Create file handler and set level to DEBUG
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # # Add formatter to handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)  # 64 KB chunks
            if not data:
                break
            #    print(file_path, data)
            hasher.update(data)
    return hasher.hexdigest()

def check_arguments(args):
    if len(args) != 4:
        print(f"Error: to sync please run: python3 sync.py <source folder> <replica folder> <interval in seconds>.")
        exit()

    if check_folder_exists(args[1]) == False:
        print(f"Error: Invalid source folder.")
        exit()

    if check_folder_exists(args[2]) == False:
        print(f"Error: Invalid replica folder.")
        exit()

    if not args[3].isdigit():
        print(f"Error: Invalid interval number.")
        exit()

def check_folder_exists(folder):
    return os.path.exists(folder)

def delete_replica_files(source_folder, replica_folder, logger, modified=0):
    # Remove files from replica that don't exist in source
    replica_files = os.listdir(replica_folder)
    for file_name in replica_files:
        replica_path = os.path.join(replica_folder, file_name)
        source_path = os.path.join(source_folder, file_name)

        if not os.path.exists(source_path):
            if os.path.isdir(replica_path):
                shutil.rmtree(replica_path)
                logger.info(f"Removed directory {file_name} from '{replica_folder}'")
            else:
                os.remove(replica_path)
                logger.info(f"Removed file {file_name} from '{replica_folder}'")
                modified += 1

    return modified

def synchronize_folders(source_folder, replica_folder, logger, modified=0):
    # Ensure replica folder exists
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # Get list of files in source folder
    source_files = os.listdir(source_folder)

    for file_name in source_files:
        source_path = os.path.join(source_folder, file_name)
        replica_path = os.path.join(replica_folder, file_name)

        if os.path.isdir(source_path):
            # Recursively synchronize subfolders
            synchronize_folders(source_path, replica_path, logger, modified)
        else:
            # Copy file if it doesn't exist in replica folder or if it's different
            if not os.path.exists(replica_path) or hash_file(source_path) != hash_file(
                replica_path
            ):
                shutil.copy2(source_path, replica_path)
                logger.info(
                    f"Copied {file_name} from '{source_folder}' to '{replica_folder}'"
                )
                modified += 1

    # Remove files from replica that don't exist in source
    modified = delete_replica_files(source_folder, replica_folder, logger, modified)

    return modified

def run():
    check_arguments(sys.argv)
    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    sync_interval_seconds = int(sys.argv[3])
    logger = setup_logger("sync.log")

    while True:
        total_files = synchronize_folders(source_folder, replica_folder, logger)

        if total_files == 0:
            logger.info(f"Nothing to update.")
        else:
            logger.info(f"All files are updated.")
        time.sleep(sync_interval_seconds)

if __name__ == "__main__":
    run()
