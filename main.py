import feedparser
import requests
from datetime import datetime, timedelta
from collections import Counter

def fetch_news(rss_urls, hours=24):
    articles = []
    cutoff = datetime.now() - timedelta(hours=hours)
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                pub = entry.get('published_parsed') or entry.get('updated_parsed')
                if pub and datetime(*pub[:6]) >= cutoff:
                    articles.append({
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'summary': entry.get('summary', '')[:200]
                    })
        except Exception:
            continue
    return articles

def rank_articles(articles, keywords):
    for art in articles:
        text = (art['title'] + ' ' + art['summary']).lower()
        art['score'] = sum(1 for kw in keywords if kw in text)
    return sorted(articles, key=lambda x: x['score'], reverse=True)[:5]

def generate_digest(top_articles):
    if not top_articles:
        return "No significant news today."
    digest = "**AI Daily Digest**\n"
    for i, art in enumerate(top_articles, 1):
        digest += f"{i}. {art['title']} - {art['link']}\n"
    return digest

def main():
    rss_urls = [
        'https://news.ycombinator.com/rss',
        'https://www.reddit.com/r/artificial/.rss'
    ]
    keywords = ['ai', 'llm', 'machine learning', 'openai', 'gpt', 'neural']
    articles = fetch_news(rss_urls, hours=24)
    top = rank_articles(articles, keywords)
    digest = generate_digest(top)
    print(digest)

if __name__ == '__main__':
    main()
