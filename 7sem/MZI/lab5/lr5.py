from gost import GOST3411
from msha1 import SHA1

message = "Hello, world".encode('utf-8')


print(f"Initial message: {message}")

# Хеш GOST34.11
gost_hash = GOST3411.hash(message)
print(f"GOST34.11 Hash:\n{bytes(gost_hash).hex()}")

# Хеш SHA-1
sha1_hash = SHA1.hash(message)
print(f"SHA-1 Hash:\n{bytes(sha1_hash).hex()}")

