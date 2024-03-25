from . import views
from django.urls import path

urlpatterns = [
    #Allan's url
    path("", views.index, name="index"),
    path("", views.navbar, name="navbar"),
    path("login/", views.login, name="login"),
    #Amone's url
    path("add_product/", views.add_product, name="add_product"),
    path("reuse/", views.reuse, name="reuse"),
    path("detail/<int:pk>/", views.get_detail, name="detail"), 
    path("search", views.search_result, name="search_result"),
    path("update/<int:pk>/", views.update, name="update_data"), 
    path("add_event", views.add_event, name="add_event"),
    path("recycle", views.recycle, name="recycle"),
]
