import argparse
from PIL import Image

# Set up argument parser
parser = argparse.ArgumentParser(description='Center an image on a custom background with a 5% margin and additional white border for Instagram.')
parser.add_argument('input_file', type=str, help='The path to the input image file')
parser.add_argument('output_file', type=str, help='The path to the output image file')
args = parser.parse_args()

# Load the original image
original_image = Image.open(args.input_file)

# Define the output size and margins
output_size = 1080
outer_margin = int(output_size * 0.01)  # 1% outer white border
inner_margin = int(output_size * 0.05)   # 5% inner margin between the border and the image

# Create a new background with the desired dark color (#1D1F22)
background_image = Image.new("RGB", (output_size, output_size), "#1D1F22")

# Calculate the aspect ratio of the original image
original_width, original_height = original_image.size
aspect_ratio = original_width / original_height

# Calculate the dimensions for the resized image, respecting the inner margin and outer white border
max_width = output_size - 2 * (inner_margin + outer_margin)
max_height = output_size - 2 * (inner_margin + outer_margin)

if aspect_ratio > 1:  # Width is the limiting factor
    new_width = max_width
    new_height = int(new_width / aspect_ratio)
else:  # Height is the limiting factor
    new_height = max_height
    new_width = int(new_height * aspect_ratio)

# Resize the original image
resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Create a new white border image
border_image = Image.new("RGB", (new_width + 2 * outer_margin, new_height + 2 * outer_margin), "white")

# Paste the resized image onto the white border
border_image.paste(resized_image, (outer_margin, outer_margin))

# Calculate the position to paste the bordered image onto the background
paste_x = (output_size - (new_width + 2 * outer_margin)) // 2
paste_y = (output_size - (new_height + 2 * outer_margin)) // 2

# Paste the bordered image onto the dark background
background_image.paste(border_image, (paste_x, paste_y))

# Save the result
background_image.save(args.output_file)

print(f"Image saved to {args.output_file}")
