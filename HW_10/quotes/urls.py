from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("tag/<str:tag>/<int:page>/", views.tags_page, name="tag_page"),
    path("author/<str:a_fullname>/", views.author_info, name="author_info"),
    path("search/", views.search, name="search_result"),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('download-data/', views.download_data, name='download_data')
    # path("search/<str:query>/<int:page>/", views.search, name="search_paginate"),
    ]
