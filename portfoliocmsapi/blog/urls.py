from rest_framework import routers
from portfoliocmsapi.blog.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"posts", PostViewSet, "post")
router.register(r"media", MediaViewSet, "media")


urlpatterns = [] + router.urls
