from gost import GOST3411
from msha1 import SHA1

message_bytes = b"010011110100101"


print(f"Initial message: {message_bytes}")

# Хеш GOST34.11
gost_hash = GOST3411.hash(message_bytes)
print(f"GOST34.11 Hash:\n{bytes(gost_hash).hex()}")

# Хеш SHA-1
sha1_hash = SHA1.hash(message_bytes)
print(f"SHA-1 Hash:\n{bytes(sha1_hash).hex()}")

