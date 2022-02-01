from django.urls import path

from . import views

# need to edit
urlpatterns = [
    path('user/', views.UserView.as_view()),
    path('entry/', views.EntryView.as_view()),
    path('archive/', views.ArchiveView.as_view())
]
