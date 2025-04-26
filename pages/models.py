from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.db.transaction import atomic

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
