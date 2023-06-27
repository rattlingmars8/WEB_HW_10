from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("tag/<str:tag>/<int:page>/", views.tags_page, name="tag_page"),
    path("author/<str:a_fullname>/", views.author_info, name="author_info"),

]
