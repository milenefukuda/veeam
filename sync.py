import os
import shutil
import hashlib
import time
import logging
import sys

# .1 criar teste unitário para função hash_file
# .2 quebrar a funçao synchronize_folders em mais funçoes e escrever testes para elas
# .3 refatorar código para que source_folder, replica_folder, sync_interval_seconds e log_file
#    sejam obrigatoriamente informados como argumento no comando, caso contrario, exiba msg de "Usage". 
#    Ex.: python sync.py source replica 1 replica.log
# .4 adicionar logs ao console output

def setup_logger(log_file):
    print(f"alooo")
    # Create logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.DEBUG)

    # return logger

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

print(f"aqui")
logger = setup_logger("replica.log")
print(f"ou aqui")

#source_folder = ""
#replica_folder = ""
#argv = len(sys.argv)

def check_folders_exists(source_folder, replica_folder):
    print(f"parei aqui 00", replica_folder, source_folder)
    if os.path.exists(source_folder) and os.path.exists(replica_folder):
        return True
    else:
        return False

def synchronize_folders(source_folder, replica_folder):
    print(f"parei aqui 01")
    print(check_folders_exists(source_folder, replica_folder))
    if False == check_folders_exists(source_folder, replica_folder):
        raise Exception("Source or Replica folder's missing, check given arguments") 
    # Get list of files in source folder
    source_files = os.listdir(source_folder)
    
    for file_name in source_files:
        source_path = os.path.join(source_folder, file_name)
        replica_path = os.path.join(replica_folder, file_name)

        if os.path.isdir(source_path):
            # Recursively synchronize subfolders
            synchronize_folders(source_path, replica_path)
        else:
            # Copy file if it doesn't exist in replica folder or if it's different
            if not os.path.exists(replica_path) or hash_file(source_path) != hash_file(replica_path):
                shutil.copy2(source_path, replica_path)
                logger.info(f"Copied {file_name} from '{source_folder}' to '{replica_folder}'")

def delete_replica_files(source_folder, replica_folder):
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

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # 64 KB chunks
            if not data:
                break
        #    print(file_path, data)
            hasher.update(data)
    return hasher.hexdigest()

# Example usage:
source_folder = "source"
replica_folder = "replica"
argv = len(sys.argv)
sync_interval_seconds = 1

def run():
    while True :
        synchronize_folders(source_folder, replica_folder)
        print("cheguei até aqui", sys.argv[0])
        time.sleep(sync_interval_seconds)

run()