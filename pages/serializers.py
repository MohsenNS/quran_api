from rest_framework import serializers
from .models import QuranPage, Khatm, KhatmRecords

class QuranPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuranPage
        fields = ['page_num', 'image']

class KhatmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khatm
        fields = '__all__'

class KhatmRecordsSerializer(serializers.ModelSerializer):
    page = QuranPageSerializer(read_only=True)

    class Meta:
        model = KhatmRecords
        fields = '__all__'