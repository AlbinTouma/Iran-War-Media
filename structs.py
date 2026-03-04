from datetime import datetime
from newspaper import Article
from pydantic import BaseModel, ConfigDict, HttpUrl, Field, field_serializer

class RSS(BaseModel):
    published_date: str | None
    source_name: str
    domain: HttpUrl | None
    title: str | None
    link: HttpUrl | None

class ScrapedArticle(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    collected_at: datetime = Field(default_factory=datetime.now)
    metadata: RSS | None
    article: Article | None

    @field_serializer('article')
    def serialize_article(self, article: Article, _info):
        # Return a dictionary or string version of the article
        return {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "url": article.url
        }
