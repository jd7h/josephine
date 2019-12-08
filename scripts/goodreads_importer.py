import csv
import re
import datetime
from django.utils import timezone

import sys, os, django
sys.path.append("josephine/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "josephine.settings")
django.setup()
from booklist.models import Book, Status, StatusUpdate, Shelf, ReadDate, Rating

def string_to_shelf(shelfname, exclusive=True):
    if exclusive: 
        model = Status
    else:
        model = Shelf
    # idea for preprocessing: translate hyphens to spaces
    shelfname = re.sub("-"," ",shelfname)
    shelves = model.objects.filter(name__startswith=shelfname)
    if shelves.count() > 0:
        return shelves[0].id
    else:
        shelf = model(name=shelfname)
        shelf.save()
        return shelf.id

def goodreads_record_to_book(record):
    # title and author
    book = Book(title=record['Title'], author=record['Author'])
    print(book)
    book.save()
    # exclusive shelf = status
    status_id = string_to_shelf(record['Exclusive Shelf'], exclusive=True)
    statusupdate = StatusUpdate(new_status_id=status_id, book_id=book.id, date=timezone.now())
    print(statusupdate)
    statusupdate.save()
    # non-exclusive shelves
    GRshelves = record['Bookshelves'].split(", ")
    # exclusive shelves are also sometimes included in this field :/
    try:
        GRshelves.remove(record['Exclusive Shelf'])
    except ValueError:
        pass # if it's not in the list, we don't care
    for GRshelf in GRshelves:
        shelf_id = string_to_shelf(GRshelf, exclusive=False)
        book.shelves.add(shelf_id)
    print(book.shelves.all())
    book.save()
    # rating
    GRrating = int(record['My Rating'])
    if GRrating > 0:
        rating = Rating(rating=GRrating, book_id=book.id)
        print(rating)
        rating.save()
    # date read (GoodReads provides only the last date read in the csv...)
    if record["Date Read"] != "":
        date_read = datetime.datetime.strptime(record["Date Read"], "%Y/%m/%d")
        date_read = timezone.make_aware(date_read) # django needs a timezone annotation
        readdate = ReadDate(date=date_read, book_id=book.id)
        print(readdate)
        readdate.save()

def main(filename="data/goodreads_library_export_example.csv"):
    data = []
    with open(filename,"r") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            data.append(row)

    for record in data:
        goodreads_record_to_book(record)

