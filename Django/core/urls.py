from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
# Schema Imports
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # JWT Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
    path('api/', include('blog_api.urls', namespace='blog_api')),

    # User Endpoints
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user', include('users.urls', namespace='users')),

    path('', include('blog.urls', namespace='blog')),

    # Schema
    path('schema', get_schema_view(
        title="Your Project",
        description="API for all things ...",
        version="1.0.0"
    ), name='openapi-schema'),

    # Docs
    path('docs/', include_docs_urls(title='BlogAPI')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)