from django.contrib import admin

# custom user model
# source: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
from .models import Book, Status, Update, ReadDate, Shelf, ReadingGoal
from .models import SitePreferences

admin.site.register(Book)
admin.site.register(Status)
admin.site.register(Update)
admin.site.register(ReadDate)
admin.site.register(Shelf)
admin.site.register(ReadingGoal)
admin.site.register(User, UserAdmin) # source: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

admin.site.register(SitePreferences)
