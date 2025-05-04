from pdf2image import convert_from_path
import os

pdf_path = "spritesheet.pdf"
output_dir = "img0"
os.makedirs(output_dir, exist_ok=True)

pages = convert_from_path(pdf_path, dpi=300)

for i, page in enumerate(pages):
    page.save(f"{output_dir}/page_{i:03}.png", "PNG")

print("Alle Seiten als PNG gespeichert.")