from PIL import Image, ImageDraw, ImageFont

# Function to generate digit images
def generate_digit_images():
    # Loop through digits 1 to 9
    for digit in range(1, 10):
        # Create a new image with white background
        img = Image.new('RGB', (50, 50), 'white')
        draw = ImageDraw.Draw(img)

        # Load a font with a size that fills the available space
        font_size = 45  # Adjust as needed
        font = ImageFont.truetype("comic.ttf", font_size)

        # Calculate text size and position
        text = str(digit)
        text_size = draw.textsize(text, font)
        text_position = ((img.width - text_size[0]) // 2, -8)

        # Draw the digit in the center
        draw.text(text_position, text, font=font, fill='black')
        
        # Draw a 2x2 black box on the bottom right corner of the image with a margin of 3 pixels
        draw.rectangle([(img.width - 4, img.height - 4), (img.width-3, img.height-3)], outline='black', width=1)
        
        # Save the image
        img.save(f'Challenge/Private/src/digits/digit_{digit}.png')

# Call the function to generate digit images
generate_digit_images()
