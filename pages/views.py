from django.shortcuts import get_object_or_404, render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, ListCreateAPIView
from .models import QuranPage, Khatm, KhatmRecords
from .serializers import QuranPageSerializer, KhatmSerializer, KhatmRecordsSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status



#generic views is used here
class QuranPageDetail(GenericAPIView):
    queryset = QuranPage.objects.all()
    serializer_class = QuranPageSerializer

    def post(self, request, *args, **kwargs):
        page_num = request.data.get('page_num')
        if page_num is None:
            return Response({"error": "page_num is required"}, status=status.HTTP_400_BAD_REQUEST)
        page = get_object_or_404(self.get_queryset(), page_num=page_num)
        serializer = self.get_serializer(page)
        return Response(serializer.data)
    
class KhatmList(ListCreateAPIView):
    queryset = Khatm.objects.all()
    serializer_class = KhatmSerializer

class KhatmDetail(RetrieveUpdateDestroyAPIView):
    queryset = Khatm.objects.all()
    serializer_class = KhatmSerializer


class KhatmRecordsList(ListCreateAPIView):
    queryset = KhatmRecords.objects.all()
    serializer_class = KhatmRecordsSerializer

class KhatmRecordsDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = KhatmRecordsSerializer

    def get_object(self):
        khatm_id = self.request.query_params.get('khatm_id')
        page_num = self.request.query_params.get('page_num')

        if not khatm_id or not page_num:
            raise NotFound("Both 'khatm_id' and 'page_num' query parameters are required.")

        try:
            # page = QuranPage.objects.get(page_num=page_num)
            return KhatmRecords.objects.select_related('page').get(
                khatm_id=khatm_id,
                page__page_num=page_num
            )
        except KhatmRecords.DoesNotExist:
            raise NotFound("KhatmRecord not found.")