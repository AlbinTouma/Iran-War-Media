from pymongo import MongoClient


class ArticlesStore():
    client = MongoClient("mongodb://albin:password1234@localhost:27017/")
    db = client['news_database']
    articles_col = db['articles']
    
    def insert_article(self, article):
        result = self.articles_col.insert_one(article)
        print(result)


