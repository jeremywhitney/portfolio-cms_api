from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/portfolio/", include("portfoliocmsapi.portfolio.urls")),
    path("api/blog/", include("portfoliocmsapi.blog.urls")),
    path("api/auth/", include("portfoliocmsapi.users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
