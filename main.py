import pdfplumber
import fitz
import os
import io
import argparse
import hashlib
from PIL import Image

# Parse arguments from terminal
parser=argparse.ArgumentParser(description="The PDF Image Extractor is a Python script designed to process PDF files, specifically extracting and saving images embedded within the pages of the document. Besides the image extraction, it also prints out the textual content of the pages.")
parser.add_argument("input_file", help="Path to the input PDF file")
parser.add_argument("--output_dir", default="extracted_images", help="Output directory for extracted images (default: extracted_images)")
parser.add_argument("--img_format", default="jpg", help="Image format (default: jpg)")
parser.add_argument("--img_quality", type=int, default=95, help="Image quality from 1-100 (default: 95)")
args=parser.parse_args()

# Define the PDF file path
PDF_PATH = args.input_file
OUTPUT_IMAGES_DIR = args.output_dir
IMAGE_FORMAT = args.img_format
IMAGE_QUALITY = args.img_quality

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)

# Global variables to track unique images
extracted_image_hashes = set()
image_counter = 1

# Resizes an image so that its width or height does not exceed the specified maximum size.
def resize_image(image):
    """
    Resizes an image so that its width or height does not exceed the specified maximum size.

    Args:
        image: The image to resize.
        max_size: The maximum size of the image, as a percentage of the larger dimension of the image.

    Returns:
        The resized image.
    """

    # Calculate the maximum size as 70% of the larger side of the image.
    max_size = int(max(image.width, image.height) * 0.7)

    if image.width > max_size or image.height > max_size:
        if image.width > image.height:
            aspect_ratio = image.height / image.width
            new_width = max_size
            new_height = int(max_size * aspect_ratio)
        else:
            aspect_ratio = image.width / image.height
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        image = image.resize((new_width, new_height), Image.BICUBIC)
    return image

# Extracts and saves all unique images from the specified page of the document.
def save_images_from_page(document, page_number):
    """
    Extracts and saves all unique images from the specified page of the document.

    Args:
        document: The PDF document.
        page_number: The page number to extract images from.

    Returns:
        A list of the filenames of the saved images.
    """
    global extracted_image_hashes, image_counter
    
    saved_images = []
    pagina = document.load_page(page_number)
    imagens = pagina.get_images(full=True)

    for img_index, img in enumerate(imagens):
        xref = img[0]
        base_image = document.extract_image(xref)
        image_bytes = base_image["image"]
        
        # Create hash of the original image bytes to detect duplicates
        image_hash = hashlib.md5(image_bytes).hexdigest()
        
        # Skip if we've already extracted this image
        if image_hash in extracted_image_hashes:
            print(f"Skipping duplicate image on page {page_number + 1}")
            continue
        
        # Convert bytes to Image and check size
        image = Image.open(io.BytesIO(image_bytes))
        if image.width < 500 or image.height < 500:
            continue

        # Resize the image
        image = resize_image(image)

        # Set the filename with simple numbering
        image_filename = os.path.join(
            OUTPUT_IMAGES_DIR, f"image_{image_counter}.{IMAGE_FORMAT}")
        
        # PIL expects "JPEG" instead of "JPG"
        pil_format = "JPEG" if IMAGE_FORMAT.lower() == "jpg" else IMAGE_FORMAT.upper()
        image.save(image_filename, pil_format, quality=IMAGE_QUALITY)

        # Track this image as extracted
        extracted_image_hashes.add(image_hash)
        saved_images.append(image_filename)
        image_counter += 1

    return saved_images

# Opens the document with fitz for image extraction.
document = fitz.open(PDF_PATH)

# Uses pdfplumber to extract text and fitz for images.
with pdfplumber.open(PDF_PATH) as pdf:
    pages = pdf.pages
    for index, pagina in enumerate(pages):
        # Extracts and prints text.
        texto = pagina.extract_text()
        print(f"Text on Page {index + 1}:")
        print(texto.strip())
        print("-" * 50)

        # Extracts and saves images.
        imagens = save_images_from_page(document, index)
        for img in imagens:
            print(f"Image Saved: {img}")
        print("=" * 50)

document.close()