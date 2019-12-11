from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Book, Shelf, Status, ReadDate, StatusUpdate, Rating
from django.db.models import Max, Q, F

def index(request):
    latest_books = Book.objects.order_by('id')[:5]
    context = {
        'latest_books' : latest_books,
    }
    return render(request, 'booklist/index.html', context)

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
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
    status = get_object_or_404(Status, pk=status_id)
    books = Book.objects\
        .annotate(last_update=Max("statusupdate__date"))\
        .filter(Q(statusupdate__new_status=status_id)&Q(statusupdate__date=F("last_update")))
    context = {
        'shelf_name' : status.name,
        'shelf_books' : books
    }
    return render(request, 'booklist/shelf.html', context)

def shelf(request, shelf_id):
    shelf = get_object_or_404(Shelf, pk=shelf_id)
    books = Book.objects.filter(shelves=shelf_id)
    context = {
        'shelf_name' : shelf.name,
        'shelf_books' : books
    }
    return render(request, 'booklist/shelf.html', context)
