# crawl.py
import praw
import json
from extract import extract_books_from_comment
from reddit_secrets import *
from validate import validate_book

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_AGENT
)

subreddit = reddit.subreddit("suggestmeabook")

def clean(text):
    return text.replace("\n", " ").strip()

def crawl_posts(limit=1000):
    count = 0
    with open("data/posts.jsonl", "w") as f:
        for post in subreddit.hot(limit=limit):
            post.comments.replace_more(limit=0)
            comments = [c.body for c in post.comments.list()[:10]]

            validated_books = []
            for c in comments:
                raw = extract_books_from_comment(c)
                for book in raw:
                    if validate_book(book):
                        validated_books.append(book)

            if not validated_books:
                continue  # Skip post if no valid book suggestions

            record = {
                "title": clean(post.title),
                "body": clean(post.selftext),
                "comments": comments,
                "suggested_books": validated_books,
                "score": post.score,
                "id": post.id,
                "url": post.url
            }
            f.write(json.dumps(record) + "\n")
            count += 1
            print(f"✅ [{count}] {post.title} — Books: {validated_books}")

if __name__ == "__main__":
    crawl_posts()
