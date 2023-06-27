import json
import os
import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HW_10.settings")
django.setup()

from quotes.models import Quotes, Tag, Author # noqa

# client = MongoClient('mongodb://localhost')
#
# db = client.hw_10
#
# authors = db.authors.find()
#
# for author in authors:
#     Author.objects.get_or_create(
#         fullname=author["author_fullname"],
#         born_date=author["author_bday"],
#         born_loc=author["author_born_loc"],
#         desc=author["author_desc"]
#     )
#
# quotes = db.quotes.find()
#
# for quote in quotes:
#     tags = []
#     for tag in quote['tags']:
#         t, *_ = Tag.objects.get_or_create(name=tag)
#         tags.append(t)
#
#     exist_quote = bool(len(Quotes.objects.filter(quote=quote['quote'])))
#
#     if not exist_quote:
#         author = db.authors.find_one({'_id': quote['author']})
#         a = Author.objects.get(fullname=author['author_fullname'])
#         q = Quotes.objects.create(
#             quote=quote['quote'],
#             author=a
#         )
#         for tag in tags:
#             q.tags.add(tag)

try:
    json_data = json.load(open('D:\PYton\DZshki\WEB\WEB_HW_10\HW_10\\utils\\authors_photos.json'))  # Загрузка данных из JSON-файла

    for i, author in enumerate(Author.objects.all()):
        photo_url = json_data.get(author.fullname,
                                  json_data.get('Unknown'))  # Получение URL-адреса фотографии по имени автора
        author.photo_url = photo_url
        author.save()
        print(i)

    print("Ссылки на фотографии успешно добавлены к авторам.")
except FileNotFoundError:
    print("Файл author_photos.json не найден.")
