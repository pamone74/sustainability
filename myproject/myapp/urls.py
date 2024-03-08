from . import views
from django.urls import path

urlpatterns = [
    path("", views.ft_try, name="ft_try"),
]
