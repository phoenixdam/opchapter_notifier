# One Piece Chapter Notifier

This script checks for the latest chapter of One Piece on [tcbonepiecechapters.com](https://tcbonepiecechapters.com/mangas/5/one-piece) and sends a notification to a Discord channel via a webhook when a new chapter is released.

## Features
- Scrapes the latest chapter information from the website.
- Sends a Discord notification when a new chapter is detected.
- Remembers the last notified chapter to avoid duplicate notifications.

## Requirements
- Python 3.7+
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Installation
1. Clone or download this repository.
2. Install dependencies:
   ```sh
   pip install requests beautifulsoup4
   ```
3. Set your Discord webhook URL as an environment variable:
   - On Windows (PowerShell):
     ```powershell
     $env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_url"
     ```
   - On Linux/macOS:
     ```sh
     export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your_webhook_url"
     ```

## Usage
Run the script:
```sh
python chapter_notifier.py
```

If a new chapter is found, a notification will be sent to your Discord channel. The script stores the last notified chapter in `last_chapter.txt`.

## Customization
- Change the `URL` variable in `chapter_notifier.py` if the source website changes.
- Adjust the Discord message format in the `send_to_discord` function as needed.

## License
MIT
