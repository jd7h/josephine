from django.db import models
import datetime

class Shelf(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "shelves"

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    shelves = models.ManyToManyField(Shelf, blank=True)

    def __str__(self):
        return self.author + " - " + self.title

    def getRatings(self):
        return Rating.objects.filter(book_id=self.id)

    def getReadDates(self):
        return ReadDate.objects.filter(book_id=self.id)

    def getCurrentStatus(self):
        return self.getStatusUpdates().latest('date')

    def getStatusUpdates(self):
        return StatusUpdate.objects.order_by('date').filter(book_id=self.id)


class Status(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "status"

    def __str__(self):
        return self.name

class StatusUpdate(models.Model):
    date = models.DateTimeField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    new_status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        date_repr = self.date.strftime("%d %b %Y")
        return date_repr + ": " + str(self.book) + " has new status " + str(self.new_status)

class ReadDate(models.Model):
    date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        date_repr = self.date.strftime("%d %b %Y")
        return date_repr + ": read " + str(self.book)

class Rating(models.Model):
    class StarRating(models.IntegerChoices):
        ONE_STAR = 1
        TWO_STARS = 2
        THREE_STARS = 3
        FOUR_STARS = 4
        FIVE_STARS = 5

    rating = models.IntegerField(choices=StarRating.choices)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.rating) + " stars for " + str(self.book)
