from django.contrib import admin
from .models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'quantity')


@admin.register(Member)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'member_id')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', 'created_at', 'issued', 'issued_at', 'returned', 'return_date', 'charges')

