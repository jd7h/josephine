from django.contrib import admin

# Register your models here.

from .models import Book, Status, StatusUpdate

admin.site.register(Book)
admin.site.register(Status)
admin.site.register(StatusUpdate)

