from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Book, Shelf, Status, ReadDate, Update

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
        'rating' : book.getRating(),
        'current_status' : book.getStatus(),
        'status_updates' : book.getUpdates(),
        'read_dates' : book.getReadDates()
    }
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

def rate(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    int_rating = int(request.POST['stars']) #post values are always a string
    try:
        star_rating = Book.StarRating(int_rating)
    except ValueError:
        return render(request, 'books/detail.html', {
            'book': book,
            'error_message': "You didn't select a valid rating for the book.",
        })
    book.rating = star_rating
    update = Update(book_id=book.id, description="has new rating " + str(star_rating) + " stars")
    book.save()
    update.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('booklist:detail', args=(book.id,)))

def status(request, status_id):
    status = get_object_or_404(Status, pk=status_id)
    books = Book.objects.filter(status=status_id)
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

def random(request):
    random_book = Book.objects.order_by('?').first() # this is slow if you're book db is large
    return HttpResponseRedirect(reverse('booklist:detail', args=(random_book.id,)))
