from django.contrib import admin

# Register your models here.

from .models import Book, Status, Update, ReadDate, Shelf, ReadingGoal

admin.site.register(Book)
admin.site.register(Status)
admin.site.register(Update)
admin.site.register(ReadDate)
admin.site.register(Shelf)
admin.site.register(ReadingGoal)
