import hashlib
import json

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file: #rb = read binary (when hashing, we need to read the file as binary)
        while True:
            data = file.read(65536) #read 65536 bytes at a time (better performance)
            if not data:
                break
            hasher.update(data) #update the hash with the data
    return hasher.hexdigest() #return the hash as a hexadecimal string

def compare_hashes(file_path, hash_value):
    file_hash = hash_file(file_path)
    return file_hash == hash_value #compare the hash of the file with the hash in the baseline

def save_baseline(file_path, hash_value):
    # Load existing baseline
    baseline = load_baseline()
    
    # Add or update the new file hash
    baseline[file_path] = hash_value
    
    # Save the updated baseline to JSON file
    with open('baseline.json', 'w') as file: #w = write (overwrite the file) (didnt use 'a' as json doesnt support appending)
        json.dump(baseline, file, indent=2) #indent=2 = pretty print the json (makes it easier to read)

def load_baseline():
    try:
        with open('baseline.json', 'r') as file: #r = read
            return json.load(file) #load the json file
    except FileNotFoundError:
        return {} #if the file doesnt exist, return an empty dictionary

def check_for_changes(file_path):
    baseline = load_baseline() #load the baseline
    if file_path in baseline: 
        if compare_hashes(file_path, baseline[file_path]): #compare the hash of the file with the hash in the baseline
            return False  # No change detected
        else:
            return True   # Change detected
    else:
        # File not in baseline, add it and report as change
        save_baseline(file_path, hash_file(file_path))
        return True
