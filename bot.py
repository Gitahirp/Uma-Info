import requests
import os
from ntscraper import Nitter

# Settings
TWITTER_USER = "umamusume_eng" # Change to the user you want
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DB_FILE = "last_tweet.txt"

scraper = Nitter()
tweets = scraper.get_tweets(TWITTER_USER, mode='user', number=1)

if tweets['tweets']:
    latest_tweet = tweets['tweets'][0]
    tweet_link = latest_tweet['link']

    # Check if we already sent this
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            if f.read().strip() == tweet_link:
                print("No new tweets.")
                exit()

    # Send to Discord
    payload = {"content": f"📢 **New Tweet from @{TWITTER_USER}:**\n{tweet_link}"}
    requests.post(WEBHOOK_URL, json=payload)

    # Save as last sent
    with open(DB_FILE, "w") as f:
        f.write(tweet_link)
