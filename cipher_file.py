# import sys
# sys.path.insert(1, '../pygost-5.13/pygost')
from Crypto.Cipher import AES
from Crypto import Random

# key = os.urandom(32) #use first run for generate key
key = b"\x10\xbb\xf0%\x1d\xb5\xc3\xb9\x91\x9d\xfe\x87\xfd\xe1\xd9\xd5\x8b\xbe\x80\xac\x8c\xb2G'Y\xec\xc7i\x9ap\xb7\x98"
print(key)
BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s)-1:])]

with open("./auth_db.sqlite", "r") as f:
    plain_text = f.read()
print(plain_text)
plain_text = pad(plain_text)
iv = Random.new().read(BS)
cipher = AES.new(key, AES.MODE_CBC, iv)
cipher_text = (iv + cipher.encrypt(plain_text.encode()))

print(cipher_text.hex())

with open("./auth_db.sqlite", "w") as f:
    f.write(cipher_text.hex())

with open("./auth_db.sqlite", "r") as f:
    cipher_text = f.read()
print(cipher_text)
print(bytes.fromhex(cipher_text))
print(type(bytes.fromhex(cipher_text)))
iv = bytes.fromhex(cipher_text)[:BS]
cipher = AES.new(key, AES.MODE_CBC, iv)
plain_text = unpad(cipher.decrypt(bytes.fromhex(cipher_text)[BS:]))
print(plain_text)
with open("./auth_db.sqlite", "w") as f:
    f.write(plain_text.decode("utf-8"))
