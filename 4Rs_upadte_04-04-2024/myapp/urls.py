from . import views
from django.urls import path
from django.contrib.auth import views as auth_views 
from .forms import LoginForm, PasswordResetForm, MySetPasswordForm, PasswordChangeForm, MyPasswordChangeForm
from django.conf import settings 
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    #Amone's url
    path("", views.home, name="home"),
    path("add_product/", views.add_product, name="add_product"),
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
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="passwordchange.html", form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),
    name="passwordchange"),
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.as_view(template_name="passwordchangedone.html"), name="passwordchangedone"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html", form_class=PasswordResetForm), name="password_reset"),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.
    as_view(template_name="password_reset_confirm.html", form_class=MySetPasswordForm), 
    name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view
    (template_name="password_reset_complete.html"), name="password_reset_complete"),



# Products and users
    path("add-reuse-product/", views.AddResueProduct.as_view(), name="add_reuse_product"),
    path("add-to-cart", views.add_product_to_cart, name="add_to_cart"),
    path("detail/<int:pk>/", views.PoductDetail, name="details"), 
    path("cart/", views.show_cart, name="cart"),
    path("reuse/", views.reuse, name="reuse"),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart", views.remove_cart, name='removecart'),
    path("checkout/", views.Checkout.as_view(), name="checkout"),
    path("my-products/", views.display_my_product, name="my_products"),
    path("update-my-products/<int:pk>", views.MyProducts.as_view(), name="update_my_products"),
    path("delete-my-products/<int:pk>", views.DeleteMyProducts.as_view(), name="delete_my_products"),


# Themes
    path("reduce/", views.reduce, name="reduce"),
    path("recycle/", views.recycle, name="recycle"),
    path("recover/", views.recover, name="recover"),
    path("create/", views.CreateProduct.as_view(), name="create"),
    path("transfer/", views.TransferProduct.as_view(), name="transfer"),
    path("create-tranfer/", views.create_tranfer, name="create-tranfer"),

#smart Bin
    # path("smartbin/", views.SmartBin.as_view(), name="smartbin"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
