from pymongo import MongoClient


class ArticlesStore():
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client['monitoring']
    articles_col = db['primary_sources']
    
    def insert_article(self, article):
        result = self.articles_col.insert_one(article)
        print(result)


    def fetch_articles(self) -> list[dict]:
        articles = self.articles_col.find()
        return list(articles)


    def upsert_article(self, article_id, result_dict):
        self.articles_col.update_one(
            {"_id": article_id},
            {"$set": result_dict},
            upsert=True
        )
