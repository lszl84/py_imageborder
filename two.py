import argparse
from PIL import Image

# Set up argument parser
parser = argparse.ArgumentParser(description='Center an image on a white background with a 1% margin for Instagram and generate two square images.')
parser.add_argument('input_file', type=str, help='The path to the input image file')
parser.add_argument('output_wide_file', type=str, help='The path to the output wide image file')
parser.add_argument('output_left_file', type=str, help='The path to the output left square image file')
parser.add_argument('output_right_file', type=str, help='The path to the output right square image file')
args = parser.parse_args()

# Load the original image
original_image = Image.open(args.input_file)

# Define the output dimensions and margin
output_width = 2 * 1080  # 2160
output_height = 1080  # 2:1 aspect ratio
margin = int(min(output_width, output_height) * 0.01)  # 1% margin

# Create a new white image with the desired dimensions
white_image = Image.new("RGB", (output_width, output_height), "white")

# Calculate the aspect ratio of the original image
original_width, original_height = original_image.size
aspect_ratio = original_width / original_height

# Calculate the dimensions for the resized image, respecting the margin
max_width = output_width - 2 * margin
max_height = output_height - 2 * margin

if aspect_ratio > (output_width / output_height):  # Width is the limiting factor
    new_width = max_width
    new_height = int(new_width / aspect_ratio)
else:  # Height is the limiting factor
    new_height = max_height
    new_width = int(new_height * aspect_ratio)

# Resize the original image
resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Calculate the position to paste the resized image
paste_x = (output_width - new_width) // 2
paste_y = (output_height - new_height) // 2

# Paste the resized image onto the white background
white_image.paste(resized_image, (paste_x, paste_y))

# Save the wide image
white_image.save(args.output_wide_file)
print(f"Wide image saved to {args.output_wide_file}")

# Split the wide image into two square images (left and right)
left_square = white_image.crop((0, 0, output_height, output_height))  # Left part
right_square = white_image.crop((output_height, 0, output_width, output_height))  # Right part

# Save the left and right square images
left_square.save(args.output_left_file)
right_square.save(args.output_right_file)

print(f"Left square image saved to {args.output_left_file}")
print(f"Right square image saved to {args.output_right_file}")
