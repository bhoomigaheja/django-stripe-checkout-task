from django.urls import path
from .views import products_page, success, cancel,signup
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", products_page, name="products"),
    path("success/", success, name="success"),  
    path("cancel/", cancel, name="cancel"),
    path("login/", auth_views.LoginView.as_view(template_name="shop/login.html"), name="login"),

    path("signup/", signup, name="signup"),    
]