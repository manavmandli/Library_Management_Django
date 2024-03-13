import datetime
from django.utils import timezone
from .models import Book,Transaction,Member


    
def getmybooks(user):
    "Get issued books or requested books of a member, takes a user & returns a tuple "
    requestedbooks=[]
    issuedbooks=[]
    if user.is_authenticated:
        member = Member.objects.filter(member_id=user).first()
        if member:
            for transaction in Transaction.objects.filter(member=member):
                book = transaction.book
                if transaction.issued:
                    issuedbooks.append(book)
                else:
                    requestedbooks.append(book)
    return [requestedbooks, issuedbooks]
