from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):  #The BookSerializer is for converting the Book models into JSON and to validate the data
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year must not be more than {current_year}")
        return value

class AuthorSerializer(serializers.ModelSerializer):  #The AuthorSerializer is for converting the Author models into JSON and to validate the data
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name', 'books']

#The relationship between Author and Book is handled by nesting a BookSerializer in the AuthorSerializer, which means an Author can have many books.