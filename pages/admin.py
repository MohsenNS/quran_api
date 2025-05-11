from django.contrib import admin
from .models import QuranPage, Khatm, KhatmRecords, Member
from django.forms import BooleanField


# Register your models here.

# admin.site.register(QuranPage)
# admin.site.register(Khatm)

# admin.site.register(KhatmRecords)

class KhatmRecordsInline(admin.TabularInline):  # or admin.StackedInline for vertical layout
    model = KhatmRecords
    extra = 0
    can_delete = False
    readonly_fields = ('page_number_display',)  # only page_number_display is readonly

    def get_fields(self, request, obj=None):
        return ('page_number_display', 'read')  # fields shown
    
    def page_number_display(self, obj):
        return obj.page.page_num
    page_number_display.short_description = 'شماره صفحه'


@admin.register(Khatm)
class KhatmAdmin(admin.ModelAdmin):
    inlines = [KhatmRecordsInline]

admin.site.register(Member)