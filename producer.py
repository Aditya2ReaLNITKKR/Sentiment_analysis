import praw
import redis
import json
import time

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent=""
)

# Redis connection (localhost works on Windows fork)
r = redis.Redis(host='localhost', port=6379, db=0)

# Stream comments from a subreddit and push to Redis
def stream_comments(subreddit_name="technology"):
    subreddit = reddit.subreddit(subreddit_name)
    print(f"Streaming comments from r/{subreddit_name}...")
    
    for comment in subreddit.stream.comments(skip_existing=True):
        comment_data = {
            "id": comment.id,
            "text": comment.body,
            "timestamp": comment.created_utc
        }
        # Push to Redis queue
        r.lpush("comments_queue", json.dumps(comment_data))
        print(f"Added comment {comment.id} to Redis queue")
        time.sleep(1)  # Throttle to avoid rate limits

if __name__ == "__main__":
    stream_comments()