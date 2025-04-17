from django.urls import path, include
from .views import QuranPageDetail, KhatmRecordsDetail

urlpatterns = [
    path('page', QuranPageDetail.as_view(), name='quran-page-detail'),
    path('khatmrecords/', KhatmRecordsDetail.as_view(), name='record-detail'),
]