from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.all, name='all'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('shelf/<int:shelf_id>/', views.shelf, name='shelf'),
    path('status/<int:status_id>/', views.status, name='status'),
]
