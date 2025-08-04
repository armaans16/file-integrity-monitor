import hashlib
import json

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def compare_hashes(file_path, hash_value):
    file_hash = hash_file(file_path)
    return file_hash == hash_value

def save_baseline(file_path, hash_value):
    # Load existing baseline
    baseline = load_baseline()
    
    # Add or update the new file hash
    baseline[file_path] = hash_value
    
    # Save the updated baseline to JSON file
    with open('baseline.json', 'w') as file:
        json.dump(baseline, file, indent=2)

def load_baseline():
    try:
        with open('baseline.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def check_for_changes(file_path):
    baseline = load_baseline()
    if file_path in baseline:
        if compare_hashes(file_path, baseline[file_path]):
            return False  # No change detected
        else:
            return True   # Change detected
    else:
        # File not in baseline, add it and report as change
        save_baseline(file_path, hash_file(file_path))
        return True
