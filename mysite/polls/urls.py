# This file is created to map the URL to the view function
from django.urls import path
from . import views

app_name = "polls" # This is the namespace for dynamically accessing the urls from another app if created
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="details"),
    path("<int:pk>/results/", views.ResultView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
   

]
