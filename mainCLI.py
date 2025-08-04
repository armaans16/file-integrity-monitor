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
            content = file.read().strip()
            if not content:  # Handle empty file
                return {}
            return json.loads(content) #load the json content
    except FileNotFoundError:
        return {} #if the file doesnt exist, return an empty dictionary
    except json.JSONDecodeError:
        return {} #if the file is corrupted, return an empty dictionary

def check_for_changes(file_path):
    baseline = load_baseline() #load the baseline
    if file_path in baseline: 
        original_hash = baseline[file_path]
        current_hash = hash_file(file_path)
        if compare_hashes(file_path, original_hash): #compare the hash of the file with the hash in the baseline
            return {"status": "unchanged", "original_hash": original_hash, "current_hash": current_hash}
        else:
            return {"status": "modified", "original_hash": original_hash, "current_hash": current_hash}
    else:
        # File not in baseline, add it
        new_hash = hash_file(file_path)
        save_baseline(file_path, new_hash)
        return {"status": "added_to_baseline", "original_hash": None, "current_hash": new_hash}

def main():
    print("\nFile Integrity Monitor")
    file_path = input("Enter absolute path to file: ")
    print("--------------------------------")
    try:
        result = check_for_changes(file_path)
        
        if result["status"] == "unchanged":
            print("File has NOT been modified")
            print(f"Original hash: {result['original_hash']}")
            print(f"Current hash:  {result['current_hash']}")
        elif result["status"] == "modified":
            print("File HAS been modified!")
            print(f"Original hash: {result['original_hash']}")
            print(f"Current hash:  {result['current_hash']}")
        elif result["status"] == "added_to_baseline":
            print("File was not in baseline. Added to baseline.")
            print(f"Current hash:  {result['current_hash']}")
            
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error: {e}")

main()