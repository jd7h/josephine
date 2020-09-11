from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Book, Shelf, Status, ReadDate, Update, ReadingGoal, SitePreferences
from django.views.generic import ListView
from django.db.models import Q
import datetime


def index(request):
    context = {}        
    if request.user.is_authenticated:
        latest_books = Book.objects.order_by('-id')[:5]
        if SitePreferences.objects.filter(user=request.user).exists():
            highlight_shelf = request.user.sitepreferences.highlight_shelf
            highlight_books = Book.objects.filter(shelves=highlight_shelf)
            context['highlight_shelf'] = highlight_shelf
            context['highlight_books'] = highlight_books
    else:
        latest_books = Book.objects.filter(isprivate=False).order_by('-id')[:5] # -id is id descending
    context['latest_books'] = latest_books
    return render(request, 'booklist/index.html', context)

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.user.is_authenticated or not book.isprivate:
        context = {
            'book' : book,
            'rating' : book.getStrRating(),
            'current_status' : book.getStatus(),
            'status_updates' : book.getUpdates(),
            'read_dates' : book.getReadDates()
        }
        return render(request, 'booklist/single.html', context)
    else:
        raise Http404("No Book matches the given query.")
    

def all(request):
    max_page_size = 100
    if request.user.is_authenticated:
        books = Book.objects.order_by('-id')
    else:
        books = Book.objects.filter(isprivate=False).order_by('-id')
    context = {
        'books' : books[:max_page_size],
    }
    return render(request, 'booklist/all.html', context)

def edit(request, book_id):
    if request.user.is_authenticated:
        return HttpResponse("You're editing book %s." % book_id)
    else:
        raise Http404("You don't have permission to edit this book.")

def rate(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.user.is_authenticated:
        int_rating = int(request.POST['stars']) #post values are always a string
        try:
            star_rating = Book.StarRating(int_rating)
        except ValueError:
            return render(request, 'booklist/single.html', {
                'book': book,
                'error_message': "You didn't select a valid rating for the book.",
            })
        book.rating = star_rating
        update = Update(book_id=book.id, description="has new rating " + str(star_rating))
        book.save()
        update.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('booklist:detail', args=(book.id,)))
    elif not request.user.is_authenticated and book.isprivate:
        raise Http404("No Book matches the given query.")
    else:
        return render(request, 'booklist/single.html', {
            'book': book,
            'error_message': "You don't have permission to edit this book.",
        })

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
    random_book = Book.objects.order_by('?').first() # this is slow if your book db is large
    return HttpResponseRedirect(reverse('booklist:detail', args=(random_book.id,)))

class SearchResultsView(ListView):
    model = Book
    template_name = 'booklist/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        return object_list

def readinggoal(request):
    thisyear = datetime.datetime.now().year
    goal = ReadingGoal.objects.filter(date_set__year=thisyear)
    readdates = ReadDate.objects.filter(date__year=thisyear)
    if goal.exists():
        return HttpResponse("Your goal is to read %d books in %d. You have read %d books so far." % (goal.first().n_books, thisyear, len(readdates)))
    else:
        return HttpResponse("You have not set a reading goal for %d." % thisyear)
