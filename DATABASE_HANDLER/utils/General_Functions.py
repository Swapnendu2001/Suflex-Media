import hashlib

def sha256_hash(input_string):
    encoded_string = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256(encoded_string)
    return sha256_hash.hexdigest()