from django.urls import path, include
from .views import QuranPageDetail, KhatmRecordsDetail
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Django Quran API",
        default_version='v1',
        description="Welcome",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('page', QuranPageDetail.as_view(), name='quran-page-detail'),
    path('khatmrecords/', KhatmRecordsDetail.as_view(), name='record-detail'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]