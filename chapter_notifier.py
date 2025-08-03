import requests
from bs4 import BeautifulSoup
import os

URL = "https://tcbonepiecechapters.com/mangas/5/one-piece"
WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

def fetch_latest_chapter():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the first chapter card
        chapter_card = soup.select_one("a.block.border.border-border.bg-card.mb-3.p-3.rounded")
        if not chapter_card:
            print("⚠️ No chapter card found. Check selector.")
            return None

        title_div = chapter_card.select_one("div.text-lg.font-bold")
        chapter_title = title_div.get_text(strip=True) if title_div else "Unknown Chapter"
        chapter_link = chapter_card["href"]

        return chapter_title, chapter_link

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

def send_to_discord(chapter_title, chapter_link):
    if not WEBHOOK:
        print("❌ Missing DISCORD_WEBHOOK_URL")
        return
    data = {
        "content": f"📢 **One Piece {chapter_title} is out!**\n🔗 <https://tcbonepiecechapters.com{chapter_link if chapter_link else ''}>"
    }
    resp = requests.post(WEBHOOK, json=data)
    if resp.status_code != 204:
        print("⚠️ Discord webhook failed:", resp.status_code)
    else:
        print("✅ Sent:", chapter_title)

def main():
    result = fetch_latest_chapter()
    if result is None:
        return
    latest_title, link = result
    last_seen = load_last_chapter()

    if latest_title != last_seen:
        send_to_discord(latest_title, link)
        save_last_chapter(latest_title)
    else:
        print("ℹ️ No new chapter:", latest_title)

if __name__ == "__main__":
    main()
