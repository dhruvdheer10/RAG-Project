from playwright.sync_api import sync_playwright
import os

urls = [
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011496/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011497/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011549/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011508/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011507/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011498/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011499/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011500/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011501/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9012695/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9012695/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9012698/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9012701/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011527/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011530/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011537/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9046383/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011539/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011540/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011546/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011553/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011558/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011561/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9011564/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9012704/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/Home?itemIdentifier=D2L.LE.Content.ContentObject.ModuleCO-9012715",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9014407/View",
    "https://brightspace.usc.edu/d2l/le/content/11082/viewContent/9012734/View",
    # "https://itsusc.service-now.com/now/nav/ui/classic/params/target/incident.do%3Fsys_id%3Da117b96a479fca54cbb0775f746d4337%26sysparm_referring_url%3Dkb_view.do"
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
