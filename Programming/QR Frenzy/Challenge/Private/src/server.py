#!/usr/bin/env python
import os
import string
import random
import signal

import base64
from io import BytesIO

import qrcode
from PIL import Image

from six.moves import input


def rotate_randomly(image):
    rotations = [0, 90, 180, 270]
    return image.rotate(random.choice(rotations))


def get_digit_image(digit):
    digit_image = Image.open(f'digits/digit_{digit}.png')
    digit_image = rotate_randomly(digit_image)
    
    return digit_image


def generate_code(content, digit):
    digit_image = get_digit_image(digit)
    
    qr_code = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    
    qr_code.add_data(content)
    qr_code.make()
    
    qr_image = qr_code.make_image()
    
    position = (
        (qr_image.size[0] - digit_image.size[0]) // 2, 
        (qr_image.size[1] - digit_image.size[1]) // 2
    )
    qr_image.paste(digit_image, position)
    
    return rotate_randomly(qr_image)
    
    
def generate_image(qr_images):
    image_width = 1920
    image_height = 1080
    
    image = Image.new("RGB", (image_width, image_height), "white")

    sub_images = []

    for qr_image in qr_images:
        qr_image_size = qr_image.size[0]

        x = random.randint(0, image_width - qr_image_size)
        y = random.randint(0, image_height - qr_image_size)

        # Prevent overlapping
        while any(
            x_check < x + qr_image_size and x < x_check + qr_image_size and y_check < y + qr_image_size and y < y_check + qr_image_size
            for x_check, y_check, _, _ in sub_images
        ):
            x = random.randint(0, image_width - qr_image_size)
            y = random.randint(0, image_height - qr_image_size)

        image.paste(qr_image, (x, y))
        sub_images.append((x, y, x + qr_image_size, y + qr_image_size))

    return image
    
    
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


def timeout_handler(signum, frame):
    raise TimeoutError("Timeout expired")


def get_input_with_timeout(prompt, timeout):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        user_input = input(prompt)
        return user_input
    except TimeoutError:
        print("\nToo late!")
        exit(1)
    finally:
        signal.alarm(0)



def server():
    # generate a string of 45 printable random chars
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=45))

    # split the key into 9 parts of 5 chars each
    key_parts = [key[i:i+5] for i in range(0, len(key), 5)]

    qr_images = [generate_code(key_parts[i], i+1) for i in range(0, 9)]
    image = generate_image(qr_images)

    b64_image = image_to_base64(image)

    print(f"You are our last hope, do well and restore order to the digital realm. Here are the codes :\n{b64_image.decode()}\n")

    answer = get_input_with_timeout("Enter the key, and save us all: ", 10)

    if answer == key:
        print(os.environ["FLAG"])
    else:
        print("That's not the key! Focus, or we will be doomed!")
        exit(1)


if __name__ == "__main__":
    server()
