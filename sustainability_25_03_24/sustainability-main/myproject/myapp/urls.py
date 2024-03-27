from . import views
from django.urls import path
from django.contrib.auth import views as auth_views 
from .forms import LoginForm, PasswordResetForm, MySetPasswordForm, PasswordChangeForm
from django.conf import settings 
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    #Amone's url
    path("", views.home, name="home"),
    path("add_product/", views.add_product, name="add_product"),
    path("reuse/", views.reuse, name="reuse"),
    path("detail/<int:pk>/", views.get_detail, name="detail"), 
    path("search", views.search_result, name="search_result"),
    path("update/<int:pk>/", views.update, name="update_data"), 
    path("add_event", views.add_event, name="add_event"),
    path("recycle", views.recycle, name="recycle"),

    # Authentication urls
    path("register", views.Registration.as_view(), name="register"),
    path("account/login/", auth_views.LoginView.as_view(template_name="login.html", authentication_form=LoginForm), name="login"),
    path("profile/", views.Dashboard, name="profile"),
    path("address/", views.Profileview.as_view(), name="address"),
    path("index/", views.home, name="index"),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    
    path("update_profile/<int:pk>", views.UpdateInformation.as_view(), name="update_profile"),
    path("create_profile/",views.Profileview.as_view(), name="create_profile"),

    #Dashboard urls
    path("recycables/", views.Dummy, name="recycables"),
    path("analytics/", views.Analytics, name="analytics"),
    path("carbon/", views.Dummy, name="carbon"),
    path("information/", views.Information, name="information"),

# Password Reset
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="passwordchange.html", form_class=PasswordChangeForm, success_url='/passwordchangedone/'),
    name="passwordchange"),
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.as_view(template_name="passwordchangedone.html"), name="passwordchangedone"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html", form_class=PasswordResetForm), name="password_reset"),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.
    as_view(template_name="password_reset_confirm.html", form_class=MySetPasswordForm), 
    name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view
    (template_name="password_reset_complete.html"), name="password_reset_complete"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
