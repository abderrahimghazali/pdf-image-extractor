# PDF Image Extractor

A Python script that extracts unique images from PDF files and saves them.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abderrahimghazali/pdf-image-extractor.git
cd pdf-image-extractor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python main.py sample_file.pdf
```

### Advanced Usage
```bash
python main.py input.pdf --output_dir my_images --img_format png --img_quality 90
```

### Options
- `input_file`: Path to the input PDF file (required)
- `--output_dir`: Output directory for extracted images (default: `extracted_images`)
- `--img_format`: Image format - jpg, png, etc. (default: `jpg`)
- `--img_quality`: Image quality from 1-100 (default: `95`)

## Example Output

```
Text on Page 1:
Lorem ipsum dolor sit amet...
--------------------------------------------------
Image Saved: extracted_images/image_1.jpg
==================================================
Text on Page 2:
In non mauris justo...
--------------------------------------------------
Skipping duplicate image on page 2
==================================================
```

## How It Works

1. **Text Extraction**: Uses `pdfplumber` to extract and display text from each page
2. **Image Extraction**: Uses `pymupdf` (fitz) to extract images from PDF pages
3. **Duplicate Detection**: Creates MD5 hash of each image to avoid saving duplicates
4. **Image Processing**: Filters small images and resizes large ones using `Pillow`
5. **Simple Naming**: Sequential naming system (`image_1.jpg`, `image_2.jpg`, etc.)

## Requirements

- Python 3.7+
- pdfplumber
- pymupdf
- pillow
