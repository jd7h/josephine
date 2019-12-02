from django.db import models
import datetime

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.author + " - " + self.title


class Status(models.Model):
    status_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "status"

    def __str__(self):
        return self.status_name

class StatusUpdate(models.Model):
    date = models.DateTimeField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    new_status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        date_repr = self.date.strftime("%d %b %Y")
        return date_repr + ": " + str(self.book) + " has new status " + str(self.new_status)
