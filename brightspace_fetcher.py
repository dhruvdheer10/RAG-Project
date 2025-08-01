from playwright.sync_api import sync_playwright
import os

urls = [
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011496/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011497/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011549/View"
]

output_dir = "/Users/nadkar/Documents/CSC_ticketing/final_texts"
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://brightspace.usc.edu/")
    input("🔐 Log in with Duo, then press Enter here...")

    for i, url in enumerate(urls):
        try:
            print(f"\n🔗 Visiting: {url}")
            page.goto(url)
            page.wait_for_load_state("networkidle")

            # Find all iframes on the page
            iframe_elements = page.query_selector_all("iframe")

            extracted = False
            for idx, iframe in enumerate(iframe_elements):
                iframe_src = iframe.get_attribute("src")
                if not iframe_src:
                    continue

                # Convert relative path to full URL
                full_iframe_url = f"https://brightspace.usc.edu{iframe_src}"
                print(f"🔍 Checking iframe {idx+1}: {full_iframe_url}")

                iframe_page = context.new_page()
                iframe_page.goto(full_iframe_url)
                iframe_page.wait_for_load_state("networkidle")

                body_text = iframe_page.locator("body").inner_text()

                if len(body_text.strip()) > 100:
                    output_path = os.path.join(output_dir, f"module_{i+1}.txt")
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(body_text)
                    print(f"✅ Extracted content from iframe {idx+1} into {output_path}")
                    extracted = True
                    iframe_page.close()
                    break

                iframe_page.close()

            if not extracted:
                print(f"⚠️ No useful iframe content found for {url}")

        except Exception as e:
            print(f"❌ Failed on {url} due to: {e}")



    browser.close()
