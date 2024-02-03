import hashlib
from src.config import PASS_SALT


class Hasher:
    salt = PASS_SALT
    def hash_str(self, string: str)->str:
        sha256_hash = hashlib.new("sha256")
        string += self.salt
        b_string = string.encode()
        sha256_hash.update(b_string)
        sha256_hex = sha256_hash.hexdigest()
        return sha256_hex

    def check_str(self, hash_string: str, string: str)->bool:
        return hash_string == self.hash_str(string)


hasher = Hasher()