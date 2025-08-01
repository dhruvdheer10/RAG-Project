from bs4 import BeautifulSoup
import os

input_folder = "/Users/nadkar/Documents/CSC_ticketing"
output_folder = os.path.join(input_folder, "extracted_texts")

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".html"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Try to isolate only the actual training content
        # You may need to adjust this depending on the HTML structure
        content_div = soup.find("div", {"class": "d2l-fileviewer-text"})  # common Brightspace class

        if content_div:
            text = content_div.get_text(separator="\n", strip=True)
        else:
            # Fallback: get all body text
            text = soup.body.get_text(separator="\n", strip=True)

        output_path = os.path.join(output_folder, filename.replace(".html", ".txt"))
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write(text)

        print(f"✅ Extracted: {output_path}")
