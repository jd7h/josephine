import urllib.request
import sys, os, django
from time import sleep
from django.core.files import File
from booklist.models import Book, Update
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Download a cover for all books with an ISBN13."
    
    def add_arguments(self, parser):
        parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite existing covers')

    def handle(self, *args, **options):
        overwrite = options['overwrite']
        for book in Book.objects.all():
            try:
                self.download_cover(book, overwrite)
            except Exception as e:
                self.stdout.write(type(e), e)

    def download_cover(self, book, overwrite=False):
        '''
        Currently only downloads covers for books for which we know an isbn13
        '''
        if not book.ISBN13:
            self.stdout.write(self.style.WARNING("No isbn13 available for " + str(book)))
            return
        if not overwrite and book.cover:
            self.stdout.write(self.style.WARNING("Book " + str(book) + " already has a cover! No new download was attempted."))
            return
        isbn = book.ISBN13
        url = "http://covers.openlibrary.org/b/ISBN/" + urllib.parse.quote(str(isbn)) + "-L.jpg"
        try:
            filename, headers = urllib.request.urlretrieve(url) # we save the img to temp file
        except Exception as e:
            self.stdout.write(self.style.ERROR(type(e), e))
        with File(open(filename, 'rb')) as bookcover:
            if bookcover.size > 807: # openlibrary returns a file of 807 bytes if no cover is found
                book.cover.save(
                    isbn + ".jpg",
                    bookcover # Django saves the img at the right location for us
                )
                book.save()
                update = Update(book=book, description="downloaded cover from OpenLibrary.org")
                update.save()
                self.stdout.write(self.style.SUCCESS("Successfully saved a cover for " + str(book)))
            else:
                self.stdout.write(self.style.WARNING("OpenLibrary has no cover available for " + str(book)))
                return
        return
