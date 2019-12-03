from django.contrib import admin

# Register your models here.

from .models import Book, Status, StatusUpdate, ReadDate, Rating, Shelf

admin.site.register(Book)
admin.site.register(Status)
admin.site.register(StatusUpdate)
admin.site.register(ReadDate)
admin.site.register(Rating)
admin.site.register(Shelf)
