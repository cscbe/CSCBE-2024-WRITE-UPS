from PIL import Image
from pyzbar.pyzbar import decode

gif_path = "output.gif"

gif = Image.open(gif_path)
frames = []
while True:
    try:
        frames.append(gif.copy())
        gif.seek(len(frames))
    except EOFError:
        break

output = []
for frame in frames:
    decoded = decode(frame)
    hex_char = decoded[0].data.decode("utf-8")
    char = bytes.fromhex(hex_char).decode("utf-8")
    output.append(char)

print("".join(output))
