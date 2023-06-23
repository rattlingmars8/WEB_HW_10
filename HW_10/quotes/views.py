from django.shortcuts import render
from django.core.paginator import Paginator

# from .utils import get_mongodb

from .models import Quotes, Tag, Author


def main(request, page=1):
    quotes = Quotes.objects.all()
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page, "url_templates": "/"})


def tags_page(request, tag, page=1):
    quotes = Quotes.objects.filter(tags__name=tag)
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page, "url_templates": "tag", "tag": tag})
