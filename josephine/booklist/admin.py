from django.contrib import admin

# Register your models here.

from .models import Book, Status, Update, ReadDate, Shelf

admin.site.register(Book)
admin.site.register(Status)
admin.site.register(Update)
admin.site.register(ReadDate)
admin.site.register(Shelf)
