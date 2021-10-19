import csv
import re
import datetime
from django.utils import timezone

import sys, os, django
sys.path.append("josephine/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "josephine.settings")
django.setup()
from booklist.models import Book, Status, Shelf, ReadDate, Update

def string_to_shelf(shelfname, exclusive=True):
    if exclusive: 
        model = Status
    else:
        model = Shelf
    # idea for preprocessing: translate hyphens to spaces
    shelfname = re.sub("-"," ",shelfname)
    shelf, created = model.objects.get_or_create(name=shelfname)
    return shelf

def goodreads_record_to_book(record):
    # exclusive shelf = status
    status = string_to_shelf(record['Exclusive Shelf'], exclusive=True)
    # title and author
    book = Book(title=record['Title'], author=record['Author'], status=status)
    if record['Publisher'] != '':
        book.publisher = record['Publisher']
    if record['Binding'] != '':
        book.binding = record['Binding']
    if record['Original Publication Year'] != '':
        book.pubyear = int(record['Original Publication Year'])
        if book.pubyear > 0:
            book.pubdate = datetime.datetime(year=int(record['Original Publication Year']), day=1, month=1)
    if record['Number of Pages'] != '':
        book.pages = int(record['Number of Pages'])
    if record['ISBN'] != '':
        book.ISBN10 = record['ISBN']
    if record['ISBN13'] != '':
        book.ISBN13 = record['ISBN13']
    print(book)
    try:
        book.save()
    except Exception as e:
        print(book)
        print(type(e), e)
        return
    else:
        update = Update(book_id=book.id, date=timezone.now(), description="imported from GoodReads")
        update.save()
        update = Update(book_id=book.id, date=timezone.now(), description="has new status " + status.name)
        print(update)
        update.save()
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
            try:
                book.rating = Book.StarRating(GRrating)
                book.save()
                update = Update(book_id=book.id, date=timezone.now(), description="has new rating " + str(book.rating) + " stars")
                print(update)
                update.save()
            except ValueError:
                pass
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

