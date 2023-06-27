from django.db.models import Count
from django.shortcuts import render
from django.core.paginator import Paginator

# from .utils import get_mongodb

from .models import Quotes, Tag, Author
from collections import Counter


def get_popular_tags(quotes):
    all_tags = [tag.name for quote in quotes for tag in quote.tags.all()]
    tag_counter = Counter(all_tags)
    popular_tags, amount = tag_counter.most_common(10)
    return popular_tags, amount


def main(request, page=1):
    quotes = Quotes.objects.all()
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)

    popular_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]
    size = popular_tags.count() * 2

    return render(request, "quotes/index.html",
                  context={"quotes": quotes_on_page, "url_templates": "/", "popular_tags": popular_tags, "size": size})

def tags_page(request, tag, page=1):
    quotes_all = Quotes.objects.all()
    quotes = Quotes.objects.filter(tags__name=tag)
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)

    popular_tags, amount = get_popular_tags(quotes_all)  # Отримання найпопулярніших тегів
    size = amount * 2

    return render(request, "quotes/index.html",
                  context={"quotes": quotes_on_page, "url_templates": "tag", "tag": tag, "popular_tags": popular_tags,
                           "size": size})


def author_info(request, a_fullname):
    # per_page = 10
    author_inf = Author.objects.get(fullname=a_fullname)
    quotes_by_author = Quotes.objects.filter(author__fullname=a_fullname)
    # paginator = Paginator(quotes_by_author, per_page)
    # quotes_on_page = paginator.get_page(page)
    return render(request, "quotes/author_quotes.html", context={"quotes": quotes_by_author, "author_info": author_inf})
