from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Book
from django.db.models import Q


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/books_list.html'
    context_object_name = 'books'
    login_url = 'account_login'


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    login_url = 'account_login'
    permission_required = ('books.special_status',)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('reviews__author')

        return queryset    

       


class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(Q(title__icontains=query) | Q(title__icontains=query))
