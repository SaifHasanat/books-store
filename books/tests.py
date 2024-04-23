from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse
from .models import Book, Review


class BookTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass123'
        )

        self.special_permission = Permission.objects.get(
            codename="special_status"
        )

        self.book = Book.objects.create(
            title='Harry Potter',
            author='Harry',
            price='50.00'

        )
        self.review = Review.objects.create(
            book=self.book,
            author=self.user,
            review='A good review'
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'Harry')
        self.assertEqual(f'{self.book.price}', '50.00')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email='testuser@gmail.com', password='testpass123')
        response = self.client.get(reverse('books_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('books/books_list.html')
        self.assertContains(response, 'Harry Potter')

    def test_book_list_view_for_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('books_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/books/' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/books/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')

    def test_book_detail_view_with_permissions(self):
        self.client.login(email='testuser@gmail.com', password='testpass123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'A good review')
        self.assertTemplateUsed(response, 'books/book_detail.html')
