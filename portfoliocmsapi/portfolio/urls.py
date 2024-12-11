from rest_framework import routers
from portfoliocmsapi.portfolio.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"tags", TagViewSet, "tag")
router.register(r"tech_stack", TechStackViewSet, "techstack")
router.register(r"projects", ProjectViewSet, "project")


urlpatterns = [] + router.urls
