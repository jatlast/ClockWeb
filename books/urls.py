from django.urls import path
from .views import BookListView, BookDetailView, SearchResultsListView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list')
    # the fillowing syntax causes Django (under-the-hood) to add another field 
    #   called id, which becomes the primary key - accessible as either id or pk.
    , path('<uuid:pk>/', BookDetailView.as_view(), name='book_detail')
    , path('search/', SearchResultsListView.as_view(), name='search_results')
]