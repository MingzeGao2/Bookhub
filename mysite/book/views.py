from django.shortcuts import render_to_response , render, redirect
from django.http import HttpResponse
from book.models import Need, Book, User, Course, Require, Registration
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.db import connection
from sets import Set
userid = 1000000
home = "http://127.0.0.1:8000/bookhub"
def needbook (request):
    global userid
    if request.method == 'POST':
        ISBN = request.POST.get("textinput-wantbook-isbn", ' ')
        title = request.POST.get("textinput-wantbook-title",' ')
        category = request.POST.get("textinput-wantbook-category",' ')
    try:
        output = []
        neededBood = Book.objects.get(ISBN = ISBN)
        try:
            entry = Need.objects.get(book=neededBood, intention="need", user=userid)
        except ObjectDoesNotExist:
            Need.objects.create(book=neededBood, intention="need",user=userid)
            return redirect("http://127.0.0.1:8000/bookhub")
        else:
            return redirect("http://127.0.0.1:8000/bookhub")
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return redirect("http://127.0.0.1:8000/bookhub")
    return redirect("http://127.0.0.1:8000/bookhub")
def delete_from_need(request):
    global userid
    if request.method == 'POST':
        book_list = request.POST.getlist(u'delete')
        for b in book_list:
            book = Book.objects.get(ISBN=b)
            intention = Need.objects.get(book=book,intention="need",user=userid)
            intention.delete()
            intention.save()
    return redirect(home)
def delete_from_have(request):
    global userid
    if request.method == 'POST':
        book_list = request.POST.getlist(u'delete')
        for b in book_list:
            book = Book.objects.get(ISBN=b)
            intention = Need.objects.get(book=book,intention="have",user=userid)
            intention.delete()
            book.amount -=1
            book.save()
            intention.save()
    return redirect("http://127.0.0.1:8000/bookhub")
def havebook (request):
    global userid
    if request.method == 'POST':
        ISBN = request.POST.get("textinput-addbook-isbn", ' ')
        title = request.POST.get("textinput-addbook-title",' ')
        category = request.POST.get("textinput-addbook-category",' ')
    try:
        book = Book.objects.get(ISBN=ISBN)
        print book
        bookid = book.id
        cursor = connection.cursor()
        cursor.execute('SELECT amount FROM book_book WHERE id = %s',[bookid])
        amount = cursor.fetchone()
        amount = amount[0] + 1
        cursor.execute('UPDATE book_book SET amount = %s WHERE id = %s',[amount,bookid])
        print book.amount
        try:
            Need.objects.get(intention="have", user = userid, book = book)
        except:
            Need.objects.create(intention= "have",user= userid,book = book)
        else:
            return redirect("http://127.0.0.1:8000/bookhub")
        return redirect("http://127.0.0.1:8000/bookhub")
    except ObjectDoesNotExist:
        insertbook(ISBN, category, title, 1)
    else:
        return redirect("http://127.0.0.1:8000/bookhub")        
    return redirect("http://127.0.0.1:8000/bookhub")
def deletebook(request):
    if request.method == 'POST':
        ISBN = request.POST.get("isbn",' ')    
    try:
        book= Book.objects.raw('SELECT * FROM book_book WHERE ISBN = %s',[ISBN])[0]
        bookid = book.id
        title = book.title
        cursor = connection.cursor()
        cursor.execute('DELETE  FROM book_book WHERE id = %s',[bookid])
        output = "%s has been deleted."%(title)
        print "good"
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
        
def delete(request):
    template = loader.get_template('book/deletebook.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def insertbook(ISBN, Category, Title, Amount):
    global home
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO book_book (ISBN, category, title, amount) VALUES(%s, %s, %s, %s)',[ISBN, Category, Title, Amount])
    except :
        context = RequestContext(request,{
            'response' : "can't be added to books"
        })
        return HttpResponse(template.render(context))        
    else:
        return redirect(home)
    return redirect("http://127.0.0.1:8000/bookhub")
    


def insert(request):
    template = loader.get_template('book/insertbook.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
    
def need(request):
    template = loader.get_template('book/needbook.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def have(request):
    template = loader.get_template('book/havebook.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def register(request):
    password = "1"
    major = "1"
    netid = "1"
    username = "1"
    if request.method == "POST":
        password = request.POST.get("password", ' ')
        major = request.POST.get("major",' ')
        netid = request.POST.get("netid",' ')
        username = request.POST.get("username",' ')
        
    try:
        user_rv = User.objects.get(netid = netid)
    except ObjectDoesNotExist:
        try:
            User.objects.create(password=password,major=major,User_name=username,netid=netid)
        except:
            return HttpResponse("not able to register")
        else:
            return HttpResponse("successfully registrated")
    else:
        return HttpResponse("you already have registrated")
                
    
def your_books(request):
    book_list = []
    user = userid
    for entry in Need.objects.all():
        ##print entry
        if entry.user == user and entry.intention == "have":
            book_list.append(entry.book)
            print entry
    template = loader.get_template('book/your_books.html')
    context = RequestContext(request,{
        'book_list' : book_list
    })
    return HttpResponse(template.render(context))
def your_account(request):
    user = userid
    template = loader.get_template('book/your_account.html')
    context = RequestContext(request,{
        'info' : user
    })
    return HttpResponse(template.render(context))
def your_wanted_list(request):
    global userid
    book_list = []
    user = userid
    for entry in Need.objects.all():
        ##print entry
        if entry.user == user and entry.intention == "need":
            print "h"
            book_list.append(entry.book)
    template = loader.get_template('book/your_wanted_list.html')
    context = RequestContext(request,{
        'book_list' : book_list
    })
    return HttpResponse(template.render(context))
def add_books(request):
    return render(request,'book/add_books.html')
def enlargeDatabase(request):
    title=[]
    isbn=[]
    cat = "CHEM"
    bookTitle =  open('book/chem.txt','r')
    for line in bookTitle:
        title.append(line)

    bookISBN = open('book/chem.txt', 'r')
    for line in bookISBN:
        isbn.append(line)
    for i in range(len(title)):
        print isbn[i] + title[i]
    for i in range(len(title)):
        try:
            book = Book.objects.create(ISBN=isbn[i],title=title[i],category=cat,amount=0)
        except:
            return HttpResponse("failed")
        else:
            print book
    return HttpResponse("good")

def user_rank():
    book_list = []
    rank = {}
    the_one = User.objects.get(netid="mgao16")
    for entry in Need.objects.all():
        if entry.user== the_one:
            book_list.append(entry.book)
    for u in User.objects.all():
        rank[u] = 0
        for entry in Need.objects.all():
            print entry.user != the_one and entry.user == u and entry.book in book_list
            if entry.user != the_one and entry.user == u  and entry.book in book_list:
                rank[u] +=1

    sorted_rank = sorted(rank, key=rank.get)    
    return sorted_rank
        
def recommended_to_you(request):
    top_ten_user = (user_rank())[-5:]
    book_list = []
    rec_books = []
    the_user = User.objects.get(netid="mgao16")
    for entry in Need.objects.all():
        if entry.user== the_user:
            book_list.append(entry.book)
    for u in top_ten_user:
        for entry in Need.objects.all():
            if entry.user != the_user and entry.user == u  and entry.book not in book_list:
                print entry.book
                rec_books.append(entry.book)
    template = loader.get_template('book/recommended_to_you.html')
    context = RequestContext(request,{
        'book_list' : rec_books
    })
    return HttpResponse(template.render(context))
    
    
def signup(request):
    if request.method == "POST":
        username = request.POST.get("textinput-signup-username",' ')
        print username
        netid = request.POST.get("textinput-signup-netid",' ')
        major = request.POST.get("textinput-signup-major",' ')
        password = request.POST.get("passwordinput-signup-0",' ')
        print password + "is password"
        confrim = request.POST.get("passwordinput-signup-1", ' ')
        set1 = set(password.split(' '))
        set2 = set(confrim.split(' '))
        print set1
        print set2
        if set1 != set2:
            return HttpResponse("please confrim your password")
        try :
            user2 = User.objects.get(User_name = username)
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(netid = netid)
            except ObjectDoesNotExist:
                try:
                    User.objects.create(password=password,major=major,User_name=username,netid=netid)
                except:
                    return HttpResponse("not able to register")
                else:
                    return redirect("http://127.0.0.1:8000/bookhub")
                    print "good"
            else:
                return HttpResponse("you already have registrated")
        else:
            return HttpResponse("please pick another username")
    template = loader.get_template('book/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def index(request):
    template = loader.get_template('book/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def login(request):
    global userid
    if request.method == "POST":
        username = request.POST.get("textinput-login-username",' ')
        password = request.POST.get("passwordinput-login",' ')
        print username
        try:
            user = User.objects.get(User_name = username)            
            print "us"
        except ObjectDoesNotExist:
            return HttpResponse("please signup first")
        else:
            print 'no'
            confrim = user.password
            set1 = set(password.split(' '))
            set2 = set(confrim.split(' '))
            if set1 != set2:
                return HttpResponse("incorrect password or username")
            else:
                userid = user
                print userid
                return redirect("http://127.0.0.1:8000/bookhub")
    return redirect("http://127.0.0.1:8000/bookhub")

def search(request):
    if request.method == "POST":
        entry = request.POST.get(" ",' ')
    book_list = []
    is_title=0
    for c in entry:
        if ord(c) < 47 and ord(c) > 58:
            is_title = 1
    if not is_title:
        book_list.append(Book.objects.get(ISBN=entry))
    else:
        books = Book.objects.filter(title__contains=entry)
        for b in books:
            book_list.append(b)
    
    
        
        
        
