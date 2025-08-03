import requests
from bs4 import BeautifulSoup
import os

URL = "https://tcbonepiecechapters.com/mangas/5/one-piece"
WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

def fetch_latest_chapter():
    soup = BeautifulSoup(requests.get(URL).text, "html.parser")
    chapters = soup.select("div.chapters-list a")
    if not chapters:
        return None
    return chapters[0].text.strip(), chapters[0]["href"]

def load_last_chapter():
    try:
        with open("last_chapter.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_chapter(chapter_title):
    with open("last_chapter.txt", "w") as f:
        f.write(chapter_title)

def send_to_discord(chapter_title, chapter_link):
    data = {
        "content": f"📢 **One Piece {chapter_title} is out!**\n🔗 <https://tcbonepiecechapters.com{chapter_link}>"
    }
    requests.post(WEBHOOK, json=data)

def main():
    latest_title, link = fetch_latest_chapter()
    last_seen = load_last_chapter()

    if latest_title != last_seen:
        send_to_discord(latest_title, link)
        save_last_chapter(latest_title)

if __name__ == "__main__":
    main()
