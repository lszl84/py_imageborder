import argparse
from PIL import Image

# Set up argument parser
parser = argparse.ArgumentParser(description='Center an image on a white background with a 5% margin for Instagram.')
parser.add_argument('input_file', type=str, help='The path to the input image file')
parser.add_argument('output_file', type=str, help='The path to the output image file')
args = parser.parse_args()

# Load the original image
original_image = Image.open(args.input_file)

# Define the output size and margin
output_size = 1080
margin = int(output_size * 0.05)  # 5% margin

# Create a new white image with the desired dimensions
white_image = Image.new("RGB", (output_size, output_size), "white")

# Calculate the aspect ratio of the original image
original_width, original_height = original_image.size
aspect_ratio = original_width / original_height

# Calculate the dimensions for the resized image, respecting the margin
max_width = output_size - 2 * margin
max_height = output_size - 2 * margin

if aspect_ratio > 1:  # Width is the limiting factor
    new_width = max_width
    new_height = int(new_width / aspect_ratio)
else:  # Height is the limiting factor
    new_height = max_height
    new_width = int(new_height * aspect_ratio)

# Resize the original image
resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Calculate the position to paste the resized image
paste_x = (output_size - new_width) // 2
paste_y = (output_size - new_height) // 2

# Paste the resized image onto the white background
white_image.paste(resized_image, (paste_x, paste_y))

# Save the result
white_image.save(args.output_file)

print(f"Image saved to {args.output_file}")

