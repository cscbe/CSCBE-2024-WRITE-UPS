import sys
from PIL import Image
from io import BytesIO
import base64
import cv2
import numpy
import pytesseract
from pwn import *


# if len(sys.argv) < 3:
#    print(f"Usage: {sys.argv[0]} <hostname> <port>")
#    exit(1)
#
# hostname = sys.argv[1]
# port = int(sys.argv[2])

conn = remote("localhost", 1338)

# Extract the base64 from the raw output
raw_output = conn.recvuntil(b"save us all: ").decode()
base64_img = raw_output.split("\n")[1]

# Decode the base64 image
pil_img = Image.open(BytesIO(base64.b64decode(base64_img)))
img = numpy.array(pil_img)

# Detect the QR codes and decode them
qcd = cv2.QRCodeDetector()
retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)

# Initialize the key array
key = ["" for i in range(9)]

for i in range(len(points)):
    # Extract the QR code from img with the given points
    rect = cv2.boundingRect(points[i])
    cropped_qr = img[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]]

    # Crop the 50x50 pixels at the center of cropped_qr
    digit_img = cropped_qr[80:130, 80:130]

    # Rotate the digit image while the pixels at the bottom right of the image are white
    while numpy.array_equal(digit_img[46, 46], [255, 255, 255]):
        digit_img = cv2.rotate(digit_img, cv2.ROTATE_90_CLOCKWISE)

    # Extract the digit from the digit image
    digit = pytesseract.image_to_string(
        digit_img, config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789"
    ).strip()
    digit = int(digit)

    # Add the qr code value to the key at the correct index
    key[digit - 1] = decoded_info[i]

# Send the key
key = "".join(key)
conn.sendline(key.encode())

# Retrieve the flag
flag = conn.recvline().decode().strip()
print("Flag: " + flag)
