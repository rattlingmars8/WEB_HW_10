from collections import Counter

from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb://localhost")
    db = client.hw_10
    print(type(db))
    return db


def get_popular_tags(quotes):
    all_tags = [tag for quote in quotes for tag in quote.tags.all()]
    tag_counter = Counter(all_tags)
    popular_tags = tag_counter.most_common(10)
    result = [tag[0] for tag in popular_tags]
    return result