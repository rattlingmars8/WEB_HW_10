import json
from collections import Counter

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .forms import AddAuthorForm, AddQuoteForm
from .models import Quotes, Tag, Author
from .utils import get_popular_tags


def main(request, page=1):
    quotes = Quotes.objects.all().order_by("-created_at")
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)

    popular_tags = get_popular_tags(quotes)
    sizes = range(30, 9, -2)
    tags_with_sizes = list(zip(popular_tags, sizes))

    return render(request, "quotes/index.html",
                  context={"quotes": quotes_on_page, "url_templates": "/", "popular_tags": tags_with_sizes})


def tags_page(request, tag, page=1):
    quotes_all = Quotes.objects.all()
    quotes = Quotes.objects.filter(tags__name=tag)
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)

    popular_tags = get_popular_tags(quotes_all)
    sizes = range(30, 9, -2)
    tags_with_sizes = list(zip(popular_tags, sizes))

    return render(request, "quotes/index.html",
                  context={"quotes": quotes_on_page, "url_templates": "tag", "tag": tag,
                           "popular_tags": tags_with_sizes,
                           })


def author_info(request, a_fullname):
    author_inf = Author.objects.get(fullname=a_fullname)
    quotes_by_author = Quotes.objects.filter(author__fullname=a_fullname)
    return render(request, "quotes/author_quotes.html", context={"quotes": quotes_by_author, "author_info": author_inf})


def search(request):
    query = request.GET.get("query", "")
    tags = []

    if query.startswith('#') or query.startswith("%23"):  # Пошук за тегами
        tags = query.split()
        tags = [tag[1:] for tag in tags]  # Видаляємо символ '#'
        # query = "#"  # Очищуємо рядок запиту

    quotes = Quotes.objects.all()

    if not query.startswith('#'):  # Пошук за цитатою та автором
        quotes = quotes.filter(
            Q(quote__icontains=query) |
            Q(author__fullname__icontains=query)
        )

    if tags:  # Фільтруємо за кожним тегом (OR)
        tag_queries = Q()
        for tag in tags:
            tag_queries |= Q(tags__name__exact=tag)
        quotes = quotes.filter(tag_queries)

    per_page = 10
    paginator = Paginator(quotes, per_page)
    page_number = request.GET.get('page', 1)
    quotes_on_page = paginator.get_page(page_number)

    popular_tags = get_popular_tags(Quotes.objects.all())
    sizes = range(30, 9, -2)
    tags_with_sizes = list(zip(popular_tags, sizes))

    context = {
        "quotes": quotes_on_page,
        "url_templates": "search",
        "popular_tags": tags_with_sizes,
        "query": query,
        "page": page_number
    }

    if query:  # Додаємо параметри пошуку до контексту
        context['query'] = query

    if tags:  # Додаємо параметри пошуку за тегами до контексту
        context['tags'] = ' '.join(['#' + tag for tag in tags])

    return render(request, "quotes/search_res.html", context)


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Перенаправление на страницу результатов поиска
    else:
        form = AddAuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_quote(request):
    authors = Author.objects.all()

    if request.method == 'POST':
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AddQuoteForm()

    context = {'form': form, "author": authors}
    return render(request, 'quotes/add_quote.html', context)


@login_required
def download_data(request):
    quotes = Quotes.objects.all()
    data = []

    for quote in quotes:
        author = quote.author
        author_data = {
            'fullname': author.fullname,
            'birthdate': author.born_date,
            'born_location': author.born_loc,
            'description': author.desc
        }

        quote_data = {
            'quote': quote.quote,
            'author': author_data,
            'tags': [tag.name for tag in quote.tags.all()],
        }

        data.append(quote_data)

    json_data = json.dumps(data)

    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="quotes_data.json"'
    return response
