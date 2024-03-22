from io import BytesIO

import qrcode
from PIL import Image


def generate_qr_code(char):
    hex_representation = hex(ord(char))[
        2:
    ]  # Get hex representation of the character without '0x' prefix
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(hex_representation)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img


def generate_gif(text):
    chars = list(text)
    images = []
    for char in chars:
        qr_image = generate_qr_code(char)
        byte_io = BytesIO()
        qr_image.save(byte_io, "PNG")
        byte_io.seek(0)
        images.append(Image.open(byte_io))

    images[0].save(
        "output.gif", save_all=True, append_images=images[1:], duration=50, loop=0
    )


input_text = "Here is a long text that is only designed to annoy you. I mean it shouldn't be that annoying as you are supposed to automate the extraction of the text and not scan each code one by one. I sure hope you didn't do that because that would be a massive waste of time. While you are here, just grab the flag: CSC{I_sUr3_hOpe_you_l1ked_Th3_movi3}. I know that no one is going to read this but I am just gonna keep on writing just to be a little more annoying."
generate_gif(input_text)
