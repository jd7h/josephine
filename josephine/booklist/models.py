from django.conf import settings
from django.db import models
from languages.fields import LanguageField
from datetime import datetime

class Shelf(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "shelves"

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "status"

    def __str__(self):
        return self.name

def get_default_status():
    return Status.objects.get_or_create(name="to read")[0].id

class Book(models.Model):
    class StarRating(models.IntegerChoices):
        ONE_STAR = 1
        TWO_STARS = 2
        THREE_STARS = 3
        FOUR_STARS = 4
        FIVE_STARS = 5

        def __str__(self):
            if self == 1:
                return str(self.value) + " star"
            else:
                return str(self.value) + " stars"

    # mandatory fields
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    status = models.ForeignKey('Status',default=get_default_status, on_delete=models.SET_DEFAULT)

    # optional fields
    orig_title = models.CharField(max_length=255, blank=True)
    ISBN13 = models.CharField(max_length=13, unique=True, blank=True, null=True)
    ISBN10 = models.CharField(max_length=10, unique=True, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    pubdate = models.DateField(blank=True, null=True)
    binding = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=2000, blank=True)
    lang = LanguageField(blank=True, null=True, max_length=10)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    shelves = models.ManyToManyField(Shelf, blank=True)

    rating = models.IntegerField(choices=StarRating.choices, blank=True, null=True)

    isprivate = models.BooleanField(default=False)

    def __str__(self):
        return self.author + " - " + self.title

    def getRating(self):
        return self.rating

    def getStrRating(self):
        if self.rating:
            return str(Book.StarRating(self.rating))
        return ''

    def getReadDates(self):
        return ReadDate.objects.filter(book_id=self.id)

    def getStatus(self):
        return self.status

    def getUpdates(self):
        return Update.objects.filter(book_id=self.id)
        
    def getPages(self):
        if self.pages:
            return self.pages
        else:
            return 0


class ReadDate(models.Model):
    date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        date_repr = self.date.strftime("%d %b %Y")
        return date_repr + ": read " + str(self.book)

class Update(models.Model):
    date = models.DateTimeField(default=datetime.now)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    def __str__(self):
        date_repr = self.date.strftime("%d %b %Y")
        return date_repr + ": " + str(self.book) + ": " + self.description

class ReadingGoal(models.Model):
    n_books = models.PositiveIntegerField()
    date_set = models.DateTimeField(default=datetime.now)

class SitePreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    highlight_shelf = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "site preferences"
