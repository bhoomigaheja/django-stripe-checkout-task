from django.urls import path
from .views import products_page, success, cancel

urlpatterns = [
    path("", products_page, name="products"),
    path("success/", success, name="success"),   # 👈 yeh zaroor hona chahiye
    path("cancel/", cancel, name="cancel"),     # 👈 yeh bhi
]