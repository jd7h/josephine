import urllib.request
import sys, os, django
from time import sleep
sys.path.append("josephine/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "josephine.settings")
django.setup()
from django.core.files import File
from booklist.models import Book, Update

def download_cover(book, overwrite=False):
    '''
    Currently only downloads covers for books for which we know an isbn13
    method copied from: https://stackoverflow.com/questions/1308386/programmatically-saving-image-to-django-imagefield
    '''
    if not book.ISBN13:
        raise ValueError("No isbn13 available for " + str(book))
    if book.cover and not overwrite:
        raise Warning("Book " + str(book) + " already has a cover! No new download was attempted.")
    isbn = book.ISBN13
    url = "http://covers.openlibrary.org/b/ISBN/" + urllib.parse.quote(str(isbn)) + "-L.jpg"
    try:
        filename, headers = urllib.request.urlretrieve(url) # we save the img to temp file
    except Exception as e:
        print(type(e), e)
    with File(open(filename, 'rb')) as bookcover:
        if bookcover.size > 807: # openlibrary returns a file of 807 bytes if no cover is found
            book.cover.save(
                isbn + ".jpg",
                bookcover # Django saves the img at the right location for us
            )
            update = Update(book=book, description="downloaded cover from OpenLibrary.org")
            update.save()
            print("Successfully saved a cover for " + str(book))
        else:
            raise ValueError("OpenLibrary has no cover available for " + str(book))
    sleep(1)
    return filename, headers

def download_all_covers():
    for book in Book.objects.all():
        try:
            download_cover(book)    
        except Exception as e:
            print(e)
            pass
