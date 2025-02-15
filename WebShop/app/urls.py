from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .forms import LoginForm

urlpatterns = [
    path("", views.ProductView.as_view(), name="home"),
    path(
        "product-detail/<int:pk>",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="showcart"),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),
    path("buy/", views.buy_now, name="buy-now"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("orders/", views.orders, name="orders"),
    path("mobile/", views.mobile, name="mobile"),
    path("mobile/<slug:data>", views.mobile, name="mobiledata"),
    path("laptop/", views.laptop, name="laptop"),
    path("laptop/<slug:data>", views.laptop, name="laptopdata"),
    path("camera/", views.camera, name="camera"),
    path("camera/<slug:data>", views.camera, name="cameradata"),
    path("watches/", views.watches, name="watches"),
    path("watches/<slug:data>", views.watches, name="watchesdata"),
    path("headphones/", views.headphones, name="headphones"),
    path("headphones/<slug:data>", views.headphones, name="headphonesdata"),
    path("television/", views.television, name="television"),
    path("television/<slug:data>", views.television, name="televisiondata"),
    path("accessories/", views.accessories, name="accessories"),
    path("accessories/<slug:data>", views.accessories, name="accessoriesdata"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/", views.payment, name="payment"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="app/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "registration/",
        views.CustomerRegistrationView.as_view(),
        name="customerregistration"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
