from django.contrib import admin
from django.utils.html import mark_safe

from .models import BookDetails, StockBook


@admin.register(BookDetails)
class BookDetailsAdmin(admin.ModelAdmin):
    list_display = ("title", "cover_preview")

    def cover_preview(self, obj):
        if obj.cover_img:
            return mark_safe(f'<img src="{obj.cover_img.url}" width="50" />')
        return "[No Image]"


admin.site.register(StockBook)
