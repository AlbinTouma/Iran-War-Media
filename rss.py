import requests
import xml.etree.ElementTree as ET
from structs import RSS

def get_rss() -> list[dict]:
    print("Fetching RSS")
    r = requests.get("https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=Iran")
    print(r)

    root = ET.fromstring(r.content)
    result = []
    for i in root.findall('.//item'):
        source  = i.find('source')
        url = source.get('url', None)
        rss = {
            "published_date": i.find('pubDate').text,
            "source_name": source.text,
            "domain": url, 
            "title": i.find('title').text,
            "link": i.find('link').text,
            }
        rss = RSS(**rss)
        result.append(rss)

    return result


if __name__ == "__main__":
    print("Running")
    get_rss()
