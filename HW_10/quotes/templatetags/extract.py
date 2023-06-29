# from bson.objectid import ObjectId
# from django import template
#
# from ..models import Author
# from ..utils import get_mongodb
#
#
# register = template.Library()
#
#
# def get_author(id_):
#     author = Author.objects.get(id_)
#     return author['author_fullname']
#
#
# register.filter('author', get_author)
