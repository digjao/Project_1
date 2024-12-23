from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("renderNewEntryPage", views.renderNewEntryPage, name="renderNewEntryPage"),
    path("random", views.random, name="random"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path('delete/<str:entry>/', views.delete_entry, name='delete_entry'),

]