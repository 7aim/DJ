from django.contrib import admin

from .models import Author, Category, Post, Book, Tag, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(Comment)