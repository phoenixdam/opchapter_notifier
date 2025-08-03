import requests
from bs4 import BeautifulSoup
import os

URL = "https://tcbonepiecechapters.com/mangas/5/one-piece"
WEBHOOK =os.environ.get("DISCORD_WEBHOOK_URL")

def fetch_latest_chapter():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        chapter_card = soup.select_one("a.block.border.border-border.bg-card.mb-3.p-3.rounded")
        if not chapter_card:
            print("⚠️ No chapter card found.")
            return None

        title_div = chapter_card.select_one("div.text-lg.font-bold")
        chapter_title = title_div.get_text(strip=True) if title_div else "Unknown Chapter"
        chapter_link = chapter_card["href"]
        full_chapter_url = f"https://tcbonepiecechapters.com{chapter_link}"

        # Get the actual chapter page and scrape first real page image
        chapter_response = requests.get(full_chapter_url)
        chapter_soup = BeautifulSoup(chapter_response.text, "html.parser")

        # Find all <img> tags and select the first one that looks like a page
        img_tags = chapter_soup.select("img")
        preview_image_url = None
        for img in img_tags:
            src = img.get("src")
            if src and "op_1156" in src and "_001" in src:
                preview_image_url = src if src.startswith("http") else f"https://tcbonepiecechapters.com{src}"
                break

        if not preview_image_url:
            print(f"⚠️ No preview image found for {chapter_title}")

        return chapter_title, chapter_link, preview_image_url

    except Exception as e:
        print(f"❌ Error while fetching latest chapter: {e}")
        return None


def load_last_chapter():
    try:
        with open("last_chapter.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_chapter(chapter_title):
    with open("last_chapter.txt", "w", encoding="utf-8") as f:
        f.write(chapter_title)

def send_to_discord(chapter_title, chapter_link, preview_image_url):
    if not WEBHOOK:
        print("❌ Missing DISCORD_WEBHOOK_URL")
        return

    if not preview_image_url:
        print(f"⚠️ Skipping embed image due to missing preview for {chapter_title}")

    full_url = f"https://tcbonepiecechapters.com{chapter_link}"

    embed = {
        "title": f"📘 {chapter_title} is out!",
        "description": f"[**Click here to read**]({full_url})",
        "color": 0x00b0f4,
        "footer": {
            "text": "Provided by TCB Scans • Set sail for greatness 🌊"}
    }

    if preview_image_url:
        embed["image"] = {"url": preview_image_url}

    data = {
        "embeds": [embed]
    }

    resp = requests.post(WEBHOOK, json=data)
    if resp.status_code != 204:
        print("⚠️ Discord webhook failed:", resp.status_code, resp.text)
    else:
        print("✅ Sent:", chapter_title)

def main():
    result = fetch_latest_chapter()
    if result is None:
        return
    latest_title, link, preview_image_url = result
    last_seen = load_last_chapter()

    if latest_title != last_seen:
        send_to_discord(latest_title, link, preview_image_url)
        save_last_chapter(latest_title)
    else:
        print("ℹ️ No new chapter:", latest_title)

if __name__ == "__main__":
    main()
