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
    thisYear = datetime.datetime.now().year
    if request.user.is_authenticated:
        currently_reading = Book.objects.filter(status_id=3)
        latest_books = Book.objects.order_by('-id')[:5]
        recent_updates = Update.objects.all().order_by('-date')[:5]
        if SitePreferences.objects.filter(user=request.user).exists():
            highlight_shelf = request.user.sitepreferences.highlight_shelf
            highlight_books = Book.objects.filter(shelves=highlight_shelf)
            context['highlight_shelf'] = highlight_shelf
            context['highlight_books'] = highlight_books
        thisYearsBooks = [readdate.book for readdate in ReadDate.objects.filter(date__year=thisYear)]
    else:
        publicBooks = Book.objects.filter(isprivate=False)
        currently_reading = publicBooks.filter(status_id=3)
        latest_books = publicBooks.order_by('-id')[:5] # -id is id descending
        recent_updates = Update.objects.filter(book__isprivate=False).order_by('-date')[:5]
        #thisYearsBooks = [readdate.book for readdate in ReadDate.objects.filter(date__year=thisYear).filter(book__isprivate=False)]
        thisYearsBooks = ReadDate.objects.filter(date__year=thisYear).filter(book__isprivate=False)
    context['currently_reading'] = currently_reading
    context['latest_books'] = latest_books
    context['recent_updates'] = recent_updates
    context['reading_stats'] = { 'thisYear' : thisYear, 'numberBooks' : len(thisYearsBooks), 'numberPages' : sum([x.getPages() for x in thisYearsBooks]) }
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
    goal_and_readdates = []
    reading_goals = ReadingGoal.objects.all().order_by('-date_set')
    for goal in reading_goals:
        books_read = len(ReadDate.objects.filter(date__year=goal.date_set.year))
        goal_and_readdates.append({'success' : goal.n_books < books_read, 'percentage' : books_read / goal.n_books,  'year' : goal.date_set.year, 'goal' : goal.n_books, 'books_read' : books_read})
    if goal_and_readdates != []:
        return render(request, 'booklist/readinggoals.html', {
                'reading_goals' : goal_and_readdates,
            })
    else:
        return render(request, 'booklist/readinggoals.html', {
                'reading_goals' : [],
                'error_message': "You have not set a reading goal yet.",
            })
