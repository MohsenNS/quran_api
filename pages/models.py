from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.db.transaction import atomic
import random

class QuranPage(models.Model):
    page_num = models.IntegerField(unique=True)
    image = models.CharField(max_length=500)
    
class Khatm(TimeStampedModel):
    text = models.TextField(max_length=2000)

    def save(self, **kwargs):
        is_new = self.pk is None
        res =  super().save(**kwargs)
        if is_new:
            records = [KhatmRecords(khatm_id=self.id, page=QuranPage.objects.get(page_num=i)) for i in range(1,604)]
            with atomic():
                KhatmRecords.objects.bulk_create(records, batch_size=1000)
        return res
    class Meta:
        verbose_name = "ختم"

class KhatmRecords(TimeStampedModel):
    khatm = models.ForeignKey(Khatm, on_delete=models.CASCADE)
    page = models.ForeignKey(QuranPage, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "رکورد صفحه"

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=200)
    city = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    subscription_code = models.CharField(max_length=5, unique=True)

    def save(self, *args, **kwargs):
        if not self.subscription_code:
            while True:
                code = f"{random.randint(10000, 99999)}"
                if not Member.objects.filter(subscription_code=code).exists():
                    self.subscription_code = code
                    break
        super().save(*args, **kwargs)
