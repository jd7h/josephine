from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Book

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
    return HttpResponse("You're looking at the details of book %s." % book_id)

def all(request):
    return HttpResponse("Here you can view all books in the database")

def edit(request, book_id):
    return HttpResponse("You're editing book %s." % book_id)

def status(request, status_id):
    response = "You're looking at all books with status %s."
    return HttpResponse(response % status_id)

def shelf(request, shelf_id):
    response = "You're looking at all books in category %s."
    return HttpResponse(response % shelf_id)


