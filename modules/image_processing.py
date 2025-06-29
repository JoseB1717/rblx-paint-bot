import os
from tkinter import filedialog
from PIL import Image
import requests
from io import BytesIO
import modules.output as output
from urllib.parse import urlparse, unquote
import uuid

# Process, resize, and preserve aspect ratio of an image
def process_image(image):
    aspect_ratio = image.width / image.height

    if aspect_ratio > 1:
        new_width = 32
        new_height = int(32 / aspect_ratio)
    else:
        new_width = int(32 * aspect_ratio)
        new_height = 32
    
    image = image.resize((new_width, new_height), Image.LANCZOS)
    final_image = Image.new("RGB", (32, 32), color=(255, 255, 255))
    paste_position = ((32 - new_width) // 2, (32 - new_height) // 2)
    
    final_image.paste(image, paste_position)
    return final_image

# Process the selected image based on a file path
def process_image_from_path():
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")]
    )
    if image_path:
        image = Image.open(image_path)
        image = process_image(image)
        new_image_path = os.path.join("processed_images", os.path.basename(image_path))
        image.save(new_image_path, quality=100)
        return image, os.path.basename(image_path)
    else:
        output.printError("Invalid image file.")

# Process the selected image based on image URl
def process_image_from_url():
    image_url = input("   Enter image address: ")
    try:
        response = requests.get(image_url)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                image = Image.open(BytesIO(response.content))
                image = process_image(image)

                parsed_url = urlparse(image_url)
                filename = os.path.basename(parsed_url.path)
                filename = unquote(filename)
                
                os.makedirs("processed_images", exist_ok=True)
                new_image_path = os.path.join("processed_images", filename)
                image.save(new_image_path, quality=100)

                return image.load(), unquote(os.path.basename(urlparse(image_url).path))
            else:
                print("Invalid image format. Formats supported are: JPG, JPEG, PNG.")
        else:
            print("Failed to process image. Try something else.")
    except:
        output.printError("Invalid image URL!")

# Process random image using the picsum API
def process_random_image(image_type):
    if image_type in ["1", "01"]:
        response = requests.get("https://picsum.photos/32/32")
    elif image_type in ["2", "02"]:
        response = requests.get("https://picsum.photos/32/32?grayscale")
    elif image_type in ["3", "03"]:
        response = requests.get("https://picsum.photos/32/32?blur")
    else:
        output.printError("Invalid option!")
        
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image = process_image(image)
            
        short_uuid = str(uuid.uuid4())[:8]
        filename = f"img_{short_uuid}.png"
        os.makedirs("processed_images", exist_ok=True)
        new_image_path = os.path.join("processed_images", filename)
        image.save(new_image_path, quality=100)

        return image, filename
    else:
        output.printError("Failed to retrieve random image.")