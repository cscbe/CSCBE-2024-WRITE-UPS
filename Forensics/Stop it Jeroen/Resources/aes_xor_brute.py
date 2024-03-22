import sys
import os
import binascii
import base64
import time
import itertools

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def xor_bytes(xs: bytes, ys: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(xs, itertools.cycle(ys)))


def print_refreshing_string(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
    sys.stdout.write("\r")
    sys.stdout.flush()


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python aes_xor_brute.py <aes_base64> <key_xor_base64> <iv_xor_base64>"
        )
        return

    aes_ciphertext = base64.b64decode(sys.argv[1])
    key_xor = base64.b64decode(sys.argv[2])
    iv_xor = base64.b64decode(sys.argv[3])
    for i in range(0, 256):
        for j in range(0, 256):
            xorkey = i.to_bytes(1, "big")
            xoriv = j.to_bytes(1, "big")
            key = xor_bytes(key_xor, xorkey)
            iv = xor_bytes(iv_xor, xoriv)
            print_refreshing_string(f"XOR key: {hex(i)} XOR iv: {hex(j)}")
            try:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decryptedtext = unpad(cipher.decrypt(aes_ciphertext), AES.block_size)
                print("\n" + decryptedtext.decode("utf-8"))
            except:
                pass


if __name__ == "__main__":
    main()
