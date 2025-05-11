from django.shortcuts import get_object_or_404, render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, ListCreateAPIView, CreateAPIView
from .models import QuranPage, Khatm, KhatmRecords, Member
from .serializers import QuranPageSerializer, KhatmSerializer, KhatmRecordsSerializer, MemberSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status



#generic views is used here
class QuranPageDetail(GenericAPIView):
    queryset = QuranPage.objects.all()
    serializer_class = QuranPageSerializer
    # beta testing for seeing pages detail using page number which is not needed in production
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
        sub_code = self.request.query_params.get('sub_code')
        
        if not sub_code:
            raise NotFound("the 'sub_code' parameter is required.")

        try:
            member = Member.objects.get(subscription_code=sub_code)
        except Member.DoesNotExist:
            raise NotFound("کاربری با این کد اشتراک پیدا نشد.")
        
        khatm_record = KhatmRecords.objects.filter(read=False).select_related('page').order_by('page__page_num').first()

        if not khatm_record:
            Khatm.objects.create(text='ختم جدید')
            khatm_record = KhatmRecords.objects.filter(read=False).select_related('page').order_by('page__page_num').first()

        khatm_record.read = True
        khatm_record.save()

        return khatm_record

        
class MemberDetail(CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'sub_code': serializer.data['subscription_code']}, status=status.HTTP_201_CREATED)
