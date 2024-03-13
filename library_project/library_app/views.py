from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime,csv
from .utilities import getmybooks
from django.db.models import Count,Sum
from django.db.models import Q




def allbooks(request):
    requestedbooks,issuedbooks=getmybooks(request.user)
    allbooks=Book.objects.all()
    
    return render(request,'library/home.html',{'books':allbooks,'issuedbooks':issuedbooks,'requestedbooks':requestedbooks})
    
def signup(request):
    if request.method=='POST':
        try:
            user=User.objects.get(username=request.POST['memberID'])
            messages.success(request,'user exists already !!')
            return redirect('/student/login/')
        
        except User.DoesNotExist:
            user=User.objects.create_user(username=request.POST['memberID'],password=request.POST['password'])

            newstudent=Member.objects.create(first_name=request.POST['firstname'],last_name=request.POST['lastname'],
            member_id=user
            )

            auth.login(request,user)
            messages.success(request,'Signup successful')
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')

    else:
        return render(request,'student/signup.html',{
            "users":list(User.objects.values_list('username',flat=True))
        })
        
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(request,
                                 username=request.POST['memberID'], 
                                 password=request.POST['password'])
        print(user)                        
        if user is None:
            messages.error(request,'Invalid CREDENTIALS')
            return redirect('/student/login/')
        else:
            auth.login(request, user)
            messages.success(request,'Login successful')
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home')
    else:
        return render(request, 'student/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request,'Logout successful')
    return redirect('home')


# def sort(request):
#     sort_type=request.GET.get('sort_type')
#     sort_by=request.GET.get('sort')
#     requestedbooks,issuedbooks=getmybooks(request.user)
#     if 'author' in sort_type:
#         author_results=Author.objects.filter(name__startswith=sort_by)
#         return render(request,'library/home.html',{'author_results':author_results,'issuedbooks':issuedbooks,'requestedbooks':requestedbooks,'selected':'author'})
#     else:
#         books_results=Book.objects.filter(name__startswith=sort_by)
#         return render(request,'library/home.html',{'books_results':books_results,'issuedbooks':issuedbooks,'requestedbooks':requestedbooks,'selected':'book'})
    
    
def search(request):
    search_query=request.GET.get('search-query')
    search_by_author=request.GET.get('author')
    requestedbooks,issuedbooks=getmybooks(request.user)

    if search_by_author is not None:
        author_results=Author.objects.filter(name__icontains=search_query)
        return render(request,'library/home.html',{'author_results':author_results,'issuedbooks':issuedbooks,'requestedbooks':requestedbooks})
    else:
        books_results=Book.objects.filter(Q(name__icontains=search_query) | Q(category__icontains=search_query))
        return render(request,'library/home.html',{'books_results':books_results,'issuedbooks':issuedbooks,'requestedbooks':requestedbooks})

@login_required(login_url='/student/login/')
def addbook(request):
    authors=Author.objects.all()
    if request.method=="POST":
        name=request.POST['name']
        category=request.POST['category']
        author=Author.objects.get(id=request.POST['author'])
        image=request.FILES['book-image']
        if author is not None or author != '':
            newbook,created=Book.objects.get_or_create(name=name,image=image,category=category,author=author)
            messages.success(request,'Book - {} Added succesfully '.format(newbook.name))
            return render(request,'library/addbook.html',{'authors':authors,})
        else:
            messages.error(request,'Author not found !')
            return render(request,'library/addbook.html',{'authors':authors,})
    else:
        return render(request,'library/addbook.html',{'authors':authors})
    
@login_required(login_url='/student/login/')
def deletebook(request,bookID):
    book=Book.objects.get(id=bookID)
    messages.success(request,'Book - {} Deleted succesfully '.format(book.name))
    book.delete()
    return redirect('/')

#  ISSUES

@login_required(login_url='/student/login/')
def issuerequest(request, bookID):
    member = Member.objects.filter(member_id=request.user).first()
    if member:
        # if member.total_debt() <= 500:
            book = Book.objects.get(id=bookID)
            if book.quantity > 0: 
                issue, created = Transaction.objects.get_or_create(book=book, member=member)
                book.quantity -= 1 
                book.save()
                messages.success(request, f'Book - {book.name} Requested successfully')
                return redirect('home')
            else:
                messages.error(request, f'No copies of {book.name} available.')
        # else:
        #     messages.error(request, 'Your outstanding debt exceeds Rs. 500. Please clear your dues.')
    else:
        messages.error(request, 'You are not a member.')
    return redirect('/')


@login_required(login_url='/student/login/')
def myissues(request):
    if Member.objects.filter(member_id=request.user).exists():
        member = Member.objects.get(member_id=request.user)
        
        if request.GET.get('issued') is not None:
            issues = Transaction.objects.filter(member=member, issued=True, returned=False)
        elif request.GET.get('notissued') is not None:
            issues = Transaction.objects.filter(member=member, issued=False)
        else:
            issues = Transaction.objects.filter(member=member)

        return render(request, 'library/myissues.html', {'issues': issues})
    
    messages.error(request, 'You are Not a Member!')
    return redirect('/')



@login_required(login_url='/admin/')
def requestedissues(request):
    if request.GET.get('memberID') is not None and request.GET.get('memberID') != '':
        try:
            user= User.objects.get(username=request.GET.get('memberID'))
            member=Member.objects.filter(member_id=user).first()
            if member:
                issues = Transaction.objects.filter(member=member, issued=False)
                return render(request, 'library/allissues.html', {'issues': issues})
            else:
                messages.error(request, 'No Member found')
                return render(request, 'library/allissues.html') 
        except User.DoesNotExist:
            messages.error(request, 'No Member found')
            return render(request, 'library/allissues.html')
    else:
        issues = Transaction.objects.filter(issued=False)
        return render(request, 'library/allissues.html', {'issues': issues})



@login_required(login_url='/admin/')
def issue_book(request,issueID):
    issue = Transaction.objects.get(id=issueID)
    if not issue.issued:  # Ensure the book is not already issued
        issue.return_date = timezone.now() + datetime.timedelta(days=7)
        issue.issued_at = timezone.now()
        issue.issued = True
        issue.save()
        return redirect('/all-issues/')
    else:
        messages.error(request, 'This book has already been issued.')

    return redirect('/all-issues/')


@login_required(login_url='/student/login/')
def return_book(request, issue_id):
    issue = Transaction.objects.get(id=issue_id)
    if issue.issued:
        issue.returned = True
        issue.return_date = timezone.now()
        days = (issue.return_date - issue.issued_at).days
        charges = max(10, days * 10)
        issue.charges = charges
        
        book = issue.book
        book.quantity += 1  # Increase available quantity when returning book
        book.save()

        issue.save()
        messages.success(request, 'Book returned successfully.')
    else:
        messages.error(request, 'This book has not been issued yet.')

    return redirect('my_issues')


def trend(request):
    popular_books = Transaction.objects.values('book__name', 'book__quantity').annotate(total_issues=Count('book')).order_by('-total_issues')[:10]
    highest_paying_customers = Transaction.objects.values('member__first_name', 'member__last_name').annotate(total_charges=Sum('charges')).order_by('-total_charges')[:10]
    
    context = {
        'popular_books': popular_books,
        'highest_paying_customers': highest_paying_customers
    }
    return render(request, 'library/trend.html', context)

def generate_report(request):
    # Fetch data from models or database
    transactions = Transaction.objects.all()
    
    # Generate report data
    report_data = []
    for transaction in transactions:
        report_data.append({
            'Member': transaction.member.first_name + ' ' + transaction.member.last_name,
            'Book': transaction.book.name,
            'Issued Date': transaction.issued_at.strftime('%Y-%m-%d'),
            'Returned': 'Yes' if transaction.returned else 'No',
            'Charges': transaction.charges
        })
    
    # Generate CSV report
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.DictWriter(response, fieldnames=['Member', 'Book', 'Issued Date', 'Returned', 'Charges'])
    writer.writeheader()
    for data in report_data:
        writer.writerow(data)

    return response

def report_view(request):
    if 'generate_report' in request.GET:
        # Fetch data from models or database
        transactions = Transaction.objects.all()
    
        # Generate report data
        report_data = []
        for transaction in transactions:
            report_data.append({
                'Member': transaction.member.first_name + ' ' + transaction.member.last_name,
                'Book': transaction.book.name,
                'Issued Date': transaction.issued_at.strftime('%Y-%m-%d'),
                'Returned': 'Yes' if transaction.returned else 'No',
                'Charges': transaction.charges
            })
        
        # Generate CSV report
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.DictWriter(response, fieldnames=['Member', 'Book', 'Issued Date', 'Returned', 'Charges'])
        writer.writeheader()
        for data in report_data:
            writer.writerow(data)

        return response

    # Fetch all transactions
    transactions = Transaction.objects.all()

    # Extract year and month from issued_at field of each transaction
    transaction_counts = {}
    for transaction in transactions:
        year = transaction.issued_at.year
        month = transaction.issued_at.month
        key = f"{year}-{month:02}" 
        if key in transaction_counts:
            transaction_counts[key] += 1
        else:
            transaction_counts[key] = 1

    data = [{'month': key, 'count': value} for key, value in transaction_counts.items()]
    return render(request, 'report.html', {'transaction_counts': data})

