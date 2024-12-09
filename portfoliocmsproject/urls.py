from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/portfolio/", include("portfoliocmsapi.portfolio.urls")),
    path("api/cms/", include("portfoliocmsapi.cms.urls")),
    path("api/auth/", include("portfoliocmsapi.users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
