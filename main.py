from playwright.sync_api import sync_playwright
from newspaper import Article
from rss import get_rss
from structs import RSS, ScrapedArticle

def give_consent(page):
    try:
        page.locator('button[jsname="b3VHJd"]').first.click()
        page.get_by_text("Accept all").first.click()
        page.wait_for_load_state("networkidle")
    except:
        pass

def create_article(page) -> Article:
    try:
        article = Article(page.url)
        article.download()
        article.parse()
        return article
    except Exception as e:
        return None

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

        s = ScrapedArticle(metadata=item, article=article)
        print(s.model_dump_json())

    browser.close()
