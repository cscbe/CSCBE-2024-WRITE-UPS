from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json
import sys

with open(sys.argv[1], 'r') as fin:
    pub_chain_str = fin.read()

pub_chain = [bytes.fromhex(b) for b in pub_chain_str.split(" ===> ")]

pub_chain = [(b[0], b[1:33], b[33:65], b[65:]) for b in pub_chain]
flag = "C"
for block_number, new_hash, prev_hash, ct in pub_chain[1:]:
    iv = ct[:16]
    ct = ct[16:]
    
    block_key = PBKDF2(prev_hash, block_number, hmac_hash_module=SHA256, count=1000000)

    cipher = AES.new(block_key, mode=AES.MODE_CBC, iv=iv)
    
    
    transations = json.loads(unpad(cipher.decrypt(ct), 16))
    flag += transations[-1]["flag"]
print(flag)