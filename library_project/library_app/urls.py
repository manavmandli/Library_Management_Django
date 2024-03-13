from django.urls import path
from .views import signup,login,logout,allbooks,search,addbook,deletebook,issuerequest,myissues,issue_book,return_book,requestedissues,trend,report_view

urlpatterns = [ 
    path('',allbooks,name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    
    path('search/',search),
    # path('sort/',sort),
    path('addbook/',addbook),
    path('deletebook/<int:bookID>/',deletebook),
    path('request-book-issue/<int:bookID>/',issuerequest),
    path('my-issues/', myissues, name='my_issues'),
    path('all-issues/',requestedissues),
    path('issuebook/<int:issueID>/',issue_book),
    path('return-book/<int:issue_id>/', return_book, name='return_book'),
    
    path('trend/',trend,name='trend'),
    path('report/', report_view, name='report_view'),
]