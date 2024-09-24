import argparse
from PIL import Image

# Set up argument parser
parser = argparse.ArgumentParser(description='Resize an image to Instagram\'s aspect ratio with a 1.5% white border and additional transparent space if needed.')
parser.add_argument('input_file', type=str, help='The path to the input image file')
parser.add_argument('output_file', type=str, help='The path to the output image file')
args = parser.parse_args()

# Load the original image
original_image = Image.open(args.input_file).convert("RGBA")  # Ensure image has alpha channel

# Get original dimensions
original_width, original_height = original_image.size

# Determine the largest side
largest_side = max(original_width, original_height)

# Calculate the 1.5% white border size
border_size = int(largest_side * 0.015)

# Add the white border to the original dimensions
new_width = original_width + 2 * border_size
new_height = original_height + 2 * border_size

# Create a new white image with RGBA and the border size
white_image = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 255))  # White background, opaque

# Paste the original image onto the white background with the border
white_image.paste(original_image, (border_size, border_size), original_image)

# Determine if the image is landscape or portrait
aspect_ratio = new_width / new_height
instagram_landscape_ratio = 16 / 9
instagram_portrait_ratio = 4 / 5

# Determine target Instagram dimensions based on orientation
if aspect_ratio > 1:  # Landscape
    target_width, target_height = 1080, 566
    instagram_ratio = instagram_landscape_ratio
else:  # Portrait
    target_width, target_height = 1080, 1350
    instagram_ratio = instagram_portrait_ratio

# Calculate the aspect ratio of the current image (with white border)
current_aspect_ratio = new_width / new_height

# Adjust for Instagram's aspect ratio by adding transparent space if necessary
if current_aspect_ratio != instagram_ratio:
    # Calculate how much transparent space to add to make the aspect ratio match Instagram's
    if current_aspect_ratio > instagram_ratio:  # Image is too wide, add transparent space to the height
        new_target_height = int(new_width / instagram_ratio)
        adjusted_image = Image.new("RGBA", (new_width, new_target_height), (0, 0, 0, 0))  # Transparent background
        # Paste the white-bordered image onto the transparent background, centered vertically
        adjusted_image.paste(white_image, (0, (new_target_height - new_height) // 2), white_image)
    else:  # Image is too tall, add transparent space to the width
        new_target_width = int(new_height * instagram_ratio)
        adjusted_image = Image.new("RGBA", (new_target_width, new_height), (0, 0, 0, 0))  # Transparent background
        # Paste the white-bordered image onto the transparent background, centered horizontally
        adjusted_image.paste(white_image, ((new_target_width - new_width) // 2, 0), white_image)
else:
    adjusted_image = white_image

# Scale the adjusted image down to Instagram's size
final_image = adjusted_image.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Save the result as a PNG (to preserve transparency)
final_image.save(args.output_file, "PNG")

print(f"Image saved to {args.output_file}")
