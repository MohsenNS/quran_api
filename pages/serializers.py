from rest_framework import serializers
from .models import QuranPage, Khatm, KhatmRecords, Member

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

class MemberSerializer(serializers.ModelSerializer):
    subscription_code = serializers.ReadOnlyField()

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'age', 'subscription_code']

class SubCodeForgottenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        help_text="Phone number without + (e.g., 98912000000)"
    )

class EitaaSubCodeForgottenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        help_text="Phone number without + (e.g., 98912000000)"
    )