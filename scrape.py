import subprocess
import json
import requests

# ----------------------------
# 사용자 설정
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1386577371666321500/3JlFCvzrC0pFC1fRh2nvR2ku1j4FTVq4j-4K2v9spUYOwcA85jM0uNnH-Wnwq7y13ALW"
ACCOUNTS = ["wannercashcow", "Fun_Viral_Vids"]
MIN_LIKES = 100    # 최소 좋아요
MIN_RETWEETS = 50  # 최소 리트윗
# ----------------------------

# Step 1: snscrape로 트윗 가져오기
tweets = []

for account in ACCOUNTS:
    command = f"python -m snscrape --jsonl twitter-user {account}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        tweet = json.loads(line)
        tweets.append(tweet)

# Step 2: 조건 필터링
high_score_tweets = []
for tweet in tweets:
    like_count = tweet.get("likeCount", 0)
    retweet_count = tweet.get("retweetCount", 0)
    content = tweet.get("content", "")
    url = tweet.get("url", "")
    media = tweet.get("media")

    if media and (like_count >= MIN_LIKES) and (retweet_count >= MIN_RETWEETS):
        high_score_tweets.append({
            "url": url,
            "content": content,
            "like": like_count,
            "retweet": retweet_count
        })

# Step 3: Discord로 알림 보내기
for tweet in high_score_tweets:
    message = {
        "content": f"🔥 **Viral Video Alert!**\n\n{tweet['content']}\n\n👉 [Tweet Link]({tweet['url']})\n👍 Likes: {tweet['like']}, 🔁 Retweets: {tweet['retweet']}"
    }
    response = requests.post(DISCORD_WEBHOOK, json=message)
    if response.status_code != 204:
        print(f"Failed to send to Discord: {response.status_code} {response.text}")

print(f"✅ Total sent: {len(high_score_tweets)} tweets")
