from . import views
from django.urls import path

urlpatterns = [
    path('', views.ft_try, name='ft_try'),
    path("add_product/", views.add_product, name="add_product"),
    path("reuse/", views.reuse, name="reuse"),
    path("detail/<int:pk>/", views.get_detail, name="detail"), 
    path("search", views.search_result, name="search_result"),
    path("update/<int:pk>/", views.update, name="update_data"), 
    path("add_event", views.add_event, name="add_event"),
    path("recycle", views.recycle, name="recycle"),
]
