import tweepy
import os
from datetime import datetime, timezone

# Текст який постимо щодня — змінюй тут
TWEET_TEXT = "Твій текст тут! 🚀"

def get_client():
    return tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )

def already_posted_today(client):
    """Перевіряє чи вже був пост сьогодні з цим текстом"""
    today = datetime.now(timezone.utc).date()

    # Отримуємо останні 10 твітів акаунту
    me = client.get_me()
    tweets = client.get_users_tweets(
        id=me.data.id,
        max_results=10,
        tweet_fields=["created_at", "text"]
    )

    if not tweets.data:
        return False

    for tweet in tweets.data:
        tweet_date = tweet.created_at.date()
        if tweet_date == today and TWEET_TEXT in tweet.text:
            print(f"✅ Сьогодні вже є пост: '{tweet.text[:50]}...'")
            return True

    return False

def post_tweet(client):
    response = client.create_tweet(text=TWEET_TEXT)
    print(f"✅ Запощено! ID твіту: {response.data['id']}")

def main():
    print(f"🤖 Бот запущено — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    client = get_client()

    if already_posted_today(client):
        print("⏭️  Пропускаємо — сьогодні вже запощено вручну або ботом.")
    else:
        print("📤 Постимо твіт...")
        post_tweet(client)

if __name__ == "__main__":
    main()
