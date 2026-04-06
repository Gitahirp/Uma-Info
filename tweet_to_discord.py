import tweepy
import requests
import os

# 1. Setup Twitter API (Using Environment Variables from GitHub Secrets)
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
api_key = os.environ.get("TWITTER_API_KEY")
api_secret = os.environ.get("TWITTER_API_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_secret = os.environ.get("TWITTER_ACCESS_SECRET")
webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

# Initialize Tweepy (v2 for basic fetching)
client = tweepy.Client(bearer_token=bearer_token)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

# The Twitter Username you want to track (without @)
twitter_username = "TARGET_ACCOUNT_HERE" 

def get_last_id():
    if os.path.exists("last_tweet_id.txt"):
        with open("last_tweet_id.txt", "r") as f:
            return f.read().strip()
    return None

def save_last_id(tweet_id):
    with open("last_tweet_id.txt", "w") as f:
        f.write(str(tweet_id))

def send_to_discord(content):
    data = {"content": content}
    requests.post(webhook_url, json=data)

# Main Logic
user = client.get_user(username=twitter_username)
user_id = user.data.id

# Fetch the most recent tweet including media details
tweets = api.user_timeline(user_id=user_id, count=1, tweet_mode='extended')

if tweets:
    latest_tweet = tweets[0]
    last_saved_id = get_last_id()

    if str(latest_tweet.id) != last_saved_id:
        # Construct the message
        tweet_text = latest_tweet.full_text
        tweet_url = f"https://twitter.com/{twitter_username}/status/{latest_tweet.id}"
        
        message = f"**New Tweet from {twitter_username}!**\n\n{tweet_text}\n\n{tweet_url}"
        
        # Check for media (Images/Videos)
        if 'extended_entities' in latest_tweet._json:
            for media in latest_tweet._json['extended_entities']['media']:
                # Adding the media URL to the message so Discord embeds it
                message += f"\n{media['media_url_https']}"

        send_to_discord(message)
        save_last_id(latest_tweet.id)
        print(f"Sent tweet {latest_tweet.id} to Discord.")
    else:
        print("No new tweets found.")
