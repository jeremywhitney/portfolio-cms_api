from rest_framework import routers
from django.urls import path
from portfoliocmsapi.auth.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, "user")


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
] + router.urls
