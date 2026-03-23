from playwright.sync_api import sync_playwright
from newspaper import Article as NewsArticle
from rss import get_rss
import json
from followthemoney import model
import nltk
from datetime import datetime, timezone
from db import ArticlesStore 

nltk.download('punkt_tab')
nltk.download('punkt')

def give_consent(page):
    try:
        page.locator('button[jsname="b3VHJd"]').first.click()
        page.get_by_text("Accept all").first.click()
        page.wait_for_load_state("networkidle")
    except:
        pass

def create_article(page) -> NewsArticle:
    try:
        article = NewsArticle(page.url)
        article.download()
        article.parse()
        return article
    except Exception as e:
        return None

def get_publisher(article):
    meta = article.meta_data
    publisher = meta.get('og', {}).get('site_name') or meta.get('publisher')
    return publisher

feed  = get_rss()
if not feed:
    print("Feed empty")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for item in feed:

        print(item.link)
        page.goto(str(item.link))
        give_consent(page)
        article = create_article(page)
        if not article:
            continue

        article.nlp()

        publisher = get_publisher(article)
        article_dict = {
                "collectionDate": str(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")),
                "processed": False,
                "title": article.title,
                "author": article.authors,
                "publishedAt": str(article.publish_date),
                "publisher": publisher, 
                "language": article.meta_lang,
                "sourceUrl":article.source_url,
                "summary":article.summary,
                "keywords": article.keywords,
                "description": article.meta_description,
                "bodyText":article.text,
#                "rawhtml": article.html,
         
                }

        
        store = ArticlesStore()
        store.insert_article(article_dict)

    browser.close()
