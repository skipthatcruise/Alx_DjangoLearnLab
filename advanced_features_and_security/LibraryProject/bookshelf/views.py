from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views import View
from .forms import ExampleForm
from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})
    raise_exception


@method_decorator(csrf_protect, name='dispatch')
class SecureView(View):
    def post(self, request):
        # Process form submission securely
        return render(request, "secure_page.html")
