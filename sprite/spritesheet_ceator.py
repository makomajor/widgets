from PIL import Image
import os
import math

# Eingabe- und Ausgabeverzeichnisse
input_dir = "img0"       # Ordner mit PNG-Dateien
output_dir = "imgout"     # Zielordner für das Spritesheet
os.makedirs(output_dir, exist_ok=True)

max_sheet_width = 2195  # maximale Breite in Pixel
max_sheet_height = 2195  # maximale Höhe in Pixel
target_size = 512  # Ausgabegröße jedes Sprites in px
sprites_per_sheet = 9  # Anzahl der Sprites pro Sheet

# Alle PNG-Dateien im Eingabeordner sammeln und sortieren
files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(".png")])
images = [Image.open(os.path.join(input_dir, f)) for f in files]

# Größe eines einzelnen Sprites (alle müssen gleich groß sein)
sprite_width, sprite_height = images[0].size
total = len(images)

columns = math.ceil(math.sqrt(sprites_per_sheet))
rows = math.ceil(sprites_per_sheet / columns)

sheet_count = math.ceil(total / sprites_per_sheet)

for sheet_index in range(sheet_count):
    # Neues Spritesheet-Bild erstellen
    sheet = Image.new("RGBA", (columns * target_size, rows * target_size))

    for i in range(sprites_per_sheet):
        global_index = sheet_index * sprites_per_sheet + i
        if global_index >= total:
            break  # fertig

        img = images[global_index]
        x = (i % columns) * target_size
        y = (i // columns) * target_size
        resized = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
        sheet.paste(resized, (x, y))

    # Speichern
    output_path = os.path.join(output_dir, f"spritesheet_{sheet_index+1:02}.png")
    sheet.save(output_path)
    print(f"✅ Spritesheet gespeichert: {output_path}")