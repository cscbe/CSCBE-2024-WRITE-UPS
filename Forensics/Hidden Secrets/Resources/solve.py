import subprocess

from pathlib import Path
from zipfile import ZipFile


zip_path = "./unknown.zip"
zip_password = "hiddensecrets"

# Extract zip file with provided password
with ZipFile(zip_path, "r") as zip:
    zip.extractall(path=".", pwd=zip_password.encode("utf-8"))

# Load file paths and sort according to number suffix
file_paths = sorted(Path(".").rglob("*.[0-9]*"), key=lambda x: int(x.name.split('.')[1]))

concat_file_name = "concatenated.ext"
# Concatenate files in right order
with open(concat_file_name, 'wb') as f:
  for p in file_paths:
    f.write(p.read_bytes())

print(f"Result written to file {concat_file_name}")

print("File type: {}".format(subprocess.check_output(f"file {concat_file_name}".split(' ')).decode().strip()))

# Concatenate file names in the right order
result = ""
for p in file_paths:
  result += p.name.split('.')[0]

print(f"Result concatenated file names: {result}")

# Try base 62 decode
# For example: https://github.com/suminb/base62/blob/develop/base62.py

BASE = 62
CHARSET_DEFAULT = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def _value(ch, charset):
  """Decodes an individual digit of a base62 encoded string."""
  try:
    return charset.index(ch)
  except ValueError:
    raise ValueError("base62: Invalid character (%s)" % ch)


def decode(encoded, charset=CHARSET_DEFAULT):
  """Decodes a base62 encoded value ``encoded``.
  :type encoded: str
  :rtype: int
  """
  l, i, v = len(encoded), 0, 0
  for x in encoded:
    v += _value(x, charset=charset) * (BASE ** (l - (i + 1)))
    i += 1
  return v

def decodebytes(encoded, charset=CHARSET_DEFAULT):
  """Decodes a string of base62 data into a bytes object.
  :param encoded: A string to be decoded in base62
  :type encoded: str
  :rtype: bytes
  """
  leading_null_bytes = b""
  while encoded.startswith("0") and len(encoded) >= 2:
    leading_null_bytes += b"\x00" * _value(encoded[1], charset)
    encoded = encoded[2:]
  decoded = decode(encoded, charset=charset)
  buf = bytearray()
  while decoded > 0:
    buf.append(decoded & 0xFF)
    decoded //= 256
  buf.reverse()
  return leading_null_bytes + bytes(buf)

decoded = decodebytes(result)

print(f"Base 62 decoded result: {decoded.decode()}")
