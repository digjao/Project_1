from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("renderNewEntryPage", views.renderNewEntryPage, name="renderNewEntryPage"),
    path("random", views.random, name="random"),
    path("saveNewPage", views.saveNewPage, name="saveNewPage"),

]