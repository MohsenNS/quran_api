from django.contrib import admin
from .models import QuranPage, Khatm, KhatmRecords

# Register your models here.

admin.site.register(QuranPage)
admin.site.register(Khatm)
admin.site.register(KhatmRecords)