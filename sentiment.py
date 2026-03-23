from db import ArticlesStore
#from textblob import TextBlob
from transformers import pipeline

class SentimentAnalyzer():
    def __init__(self):
        self.db = ArticlesStore()
        self.sentiment_analyzer = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def process_articles(self):
        articles = self.db.fetch_articles()
        for article in articles:
            if not article.get("processed", False):
                sentiment_score = self.sentiment_analyzer(
                        article['bodyText'], 
                        ["positive", "factual", "negative"]
                        )
                result_dict = {
                        "processed": True,
                        "analysis.sentiment": {
                        "tone": sentiment_score['labels'][0], 
                        "score": sentiment_score['scores'][0] 
                        }
                }
            print(f"Processing {article['_id']}: {result_dict}")
            self.db.upsert_article(article["_id"], result_dict)


SentimentAnalyzer().process_articles()
