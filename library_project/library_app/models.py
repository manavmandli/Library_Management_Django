from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

class Author(models.Model):
    name=models.CharField(max_length=350)
    description=models.CharField(max_length=450)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    name=models.CharField(max_length=350)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    image=models.ImageField()
    category=models.CharField(max_length=220)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

    
class Member(models.Model):
    first_name=models.CharField(max_length=120)
    last_name=models.CharField(max_length=120)
    member_id=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    # def total_debt(self):
    #     return sum(transaction.charges for transaction in self.transaction_set.filter(returned=False))
    
class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    issued = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(auto_now=False, auto_created=False, auto_now_add=False, null=True, blank=True)
    charges = models.DecimalField(max_digits=10, decimal_places=2, null=True)


    def __str__(self):
        return f"{self.member} - {self.book}"
