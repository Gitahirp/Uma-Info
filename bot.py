import requests
import os
from ntscraper import Nitter

# Settings
TWITTER_USER = "uma_musu_jp" 
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DB_FILE = "last_tweet.txt"

# 1. Initialize with log_level=1 to see what's happening
# 2. Skip the automatic check to prevent the IndexError crash
scraper = Nitter(log_level=1, skip_instance_check=True)

try:
    # We try a known stable instance. 
    # If poast.org fails, try 'https://nitter.privacydev.net' or 'https://xcancel.com'
    tweets = scraper.get_tweets(TWITTER_USER, mode='user', number=1, instance='https://nitter.poast.org')
    
    if tweets and 'tweets' in tweets and len(tweets['tweets']) > 0:
        latest_tweet = tweets['tweets'][0]
        tweet_link = latest_tweet['link']
        tweet_text = latest_tweet['text']

        # Duplicate Check
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                if f.read().strip() == tweet_link:
                    print("No new tweets.")
                    exit()

        # Send to Discord (Discohook style)
        payload = {
            "embeds": [{
                "title": f"New Post from @{TWITTER_USER}",
                "description": tweet_text,
                "url": tweet_link,
                "color": 16711935, # Pink color
                "footer": {"text": "Sent via GitHub Actions"}
            }]
        }
        
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Successfully sent to Discord!")
            with open(DB_FILE, "w") as f:
                f.write(tweet_link)
        else:
            print(f"Discord Error: {response.status_code}")
    else:
        print("No tweets found or account is private/empty.")

except Exception as e:
    print(f"Scraper failed: {e}")
