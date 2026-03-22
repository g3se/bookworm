from django.contrib import admin

from .models import BookDetails, StockBook


admin.site.register(BookDetails)
admin.site.register(StockBook)
