# scripts/telegram_scraper.py

import csv
import os
from dotenv import load_dotenv
from telethon import TelegramClient

# Load credentials from the .env file in the project root
load_dotenv()

api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('TG_PHONE')  # optional, not used unless login needed

# Paths relative to the root project structure
csv_path = os.path.join('data', 'telegram_data.csv')
media_dir = os.path.join('data', 'photos')
os.makedirs(media_dir, exist_ok=True)

# Initialize Telegram client with session name and credentials
client = TelegramClient('Telegram_Scraper', api_id, api_hash)

async def scrape_channel(client, channel_username, writer, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title

    async for message in client.iter_messages(entity, limit=10000):
        media_path = None

        if message.media and hasattr(message.media, 'photo'):
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            await client.download_media(message.media, media_path)

        writer.writerow([
            channel_title,
            channel_username,
            message.id,
            message.message,
            message.date,
            media_path
        ])

async def main():
    await client.start()

    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

        channels = [
            '@ZemenExpress',
            '@nevacomputer',
            '@helloomarketethiopia',
            '@modernshoppingcenter',
            '@qnashcom',
           '@gebeyaadama',
            '@Shageronlinestore'
]
        

        for channel in channels:
            print(f"Scraping {channel}...")
            await scrape_channel(client, channel, writer, media_dir)
            print(f"Finished {channel}")

# Run scraper
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
