import requests
import datetime
import json
import sys, os, django
from time import sleep
sys.path.append("josephine/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "josephine.settings")
django.setup()
from django.utils import timezone
from django.core.files import File
from booklist.models import Book, Update

def isbn2book(isbn):
    url = "http://openlibrary.org/search.json?isbn={}".format(isbn)
    result = requests.get(url)
    if result.status_code != 200:
        return
    data = json.loads(result.text)
    if data.get('num_found') < 1:
        return
    bookinfo = data.get('docs')[0]
    author = bookinfo.get('author_name')[0]
    title = bookinfo.get('title')
    first_published = bookinfo.get('first_publish_year')
    book = Book(title=title, author=author) 
    if len(isbn) == 13:
        book.ISBN13 = isbn
    elif len(isbn) == 10:
        book.ISBN10 == isbn
    if first_published:
        book.pubdate = timezone.make_aware(datetime.datetime(year=first_published, month=1, day=1))
    return book
    
def import_isbn_list(isbn_list_filename, dry_run = False):
    # open list of isbns
    with open(isbn_list_filename) as infile:
        isbns = infile.read().split("\n")
    # search openlibrary for isbns
    new_books = []
    unknown_isbns = []
    for isbn in isbns:
        book = isbn2book(isbn)
        if book:
            new_books.append(book)
        else:
            unknown_isbns.append(isbn)
    # add found books to database
    if not dry_run:
        for book in new_books:
            print("Adding {}".format(book))
            try:
                book.save()
                update = Update(book=book, description="downloaded book data from OpenLibrary.org")
                update.save()
            except Exception as e:
                print(type(e),e)
                pass
    print("Found {} books in OpenLibrary db".format(len(new_books)))
    if dry_run:
        print("Nothing saved to Josephine database, because this is a dry run")
    print()
    print("These ISBNs could not be found in the OpenLibrary db:")
    print("\n".join(unknown_isbns))
    return isbns, new_books, unknown_isbns
