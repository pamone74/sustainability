from . import views
from django.urls import path
from django.contrib.auth import views as auth_views 
from .forms import LoginForm
from django.conf import settings 
from django.conf.urls.static import static

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
    path("register", views.Registration.as_view(), name="register"),
    path("account/login/", auth_views.LoginView.as_view(template_name="login.html", authentication_form=LoginForm), name="login"),
    path("profile/", views.Profileview.as_view(), name="profile"),
    path("address/", views.Profileview.as_view(), name="address"),
    path("index/", views.index, name="index"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
