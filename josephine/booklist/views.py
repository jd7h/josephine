from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Book, Shelf, Status, ReadDate, StatusUpdate, Rating
from django.db.models import Max, Q, F

# Create your views here.
def index(request):
    latest_books = Book.objects.order_by('id')[:5]
    template = loader.get_template('booklist/index.html')
    context = {
        'latest_books' : latest_books,
    }
    output = "<br>".join([str(book) for book in latest_books])
    return HttpResponse(template.render(context, request))

def detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Question.DoesNotExist:
        raise Http404("This book does not exist")
    context = {
        'book' : book,
    }
    if ReadDate.objects.filter(book=book_id).count() > 0:
        context.update({"readdates" : ReadDate.objects.filter(book=book_id)})
    statusupdates = StatusUpdate.objects.order_by('date').filter(book=book_id)
    if statusupdates.count() > 0:
        context.update({"statusupdates" : statusupdates})
        current_status = statusupdates.latest('date')
        context.update({'current_status' : current_status})
    if Rating.objects.filter(book_id=book_id).count() > 0:
        context.update({ "rating" : Rating.objects.filter(book_id=book_id).first() })
    return render(request, 'booklist/single.html', context)

def all(request):
    max_page_size = 100
    if Book.objects.count() < max_page_size:
        books = Book.objects.order_by('id')
    else:
        books = Book.objects.order_by('id')[:max_page_size]
    context = {
        'books' : books,
    }
    return render(request, 'booklist/all.html', context)

def edit(request, book_id):
    return HttpResponse("You're editing book %s." % book_id)

def status(request, status_id):
    try:
        status = Status.objects.get(pk=status_id)
    except Status.DoesNotExist:
        raise Http404("This status does not exist")
    books = Book.objects\
        .annotate(last_update=Max("statusupdate__date"))\
        .filter(Q(statusupdate__new_status=status_id)&Q(statusupdate__date=F("last_update")))
    context = {
        'shelf_name' : status.name,
        'shelf_books' : books
    }
    return render(request, 'booklist/shelf.html', context)

def shelf(request, shelf_id):
    try:
        shelf = Shelf.objects.get(pk=shelf_id)
    except Shelf.DoesNotExist:
        raise Http404("This shelf does not exist")
    books = Book.objects.filter(shelves=shelf_id)
    context = {
        'shelf_name' : shelf.name,
        'shelf_books' : books
    }
    return render(request, 'booklist/shelf.html', context)
