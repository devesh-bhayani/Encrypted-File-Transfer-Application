import hashlib

def calculate_checksum(file_path, hash_algo='sha256'):
    """
    Calculates the checksum of a file.

    :param file_path: Path to the file.
    :param hash_algo: The hashing algorithm to use (e.g., 'sha256', 'md5').
    :return: The hexadecimal checksum string.
    """
    h = hashlib.new(hash_algo)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
