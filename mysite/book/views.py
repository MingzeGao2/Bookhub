from django.shortcuts import render_to_response , render, redirect
from django.http import HttpResponse
from book.models import Need, Book, User, Course, Require, Registration, Search
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.db import connection
from sets import Set
import random
userid = 1000000
hotness_dic = {"CS":0, "MATH":0, "HIST":0, "CHEM":0}
home = "http://127.0.0.1:8000/bookhub"
def needbook (request):
    global userid
    if request.method == 'POST':
        ISBN = request.POST.get("textinput-wantbook-isbn", ' ')
        title = request.POST.get("textinput-wantbook-title",' ')
        category = request.POST.get("textinput-wantbook-category",' ')
    try:
        output = []
        neededBood = Book.objects.get(ISBN__contains = ISBN)
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
            b = b[:-2]
            book = Book.objects.get(ISBN__contains=b)
            intention = Need.objects.get(book=book,intention="need",user=userid)
            intention.delete()
    return redirect(home)
def delete_from_have(request):
    global userid
    if request.method == 'POST':
        book_list = request.POST.getlist(u'delete')
        print book_list
        for b in book_list:
            b = b[:-2]
            book = Book.objects.filter(ISBN__contains=b)[0]
            intention = Need.objects.get(book=book,intention="have",user=userid)
            intention.delete()
            book.amount -=1
    return redirect("http://127.0.0.1:8000/bookhub")

def havebook (request):
    global userid
    if request.method == 'POST':
        ISBN = request.POST.get("textinput-addbook-isbn", ' ')
        title = request.POST.get("textinput-addbook-title",' ')
        category = request.POST.get("textinput-addbook-category",' ')
    try:
        book = Book.objects.get(ISBN__contains=ISBN)
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
    global userid
    book_list = []
    top_n = 5
    rank = {}
    the_one = userid
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM book_need')
    all_need = cursor.fetchall()
    for entry in all_need:
        if entry[3] == userid.id:
            book_list.append(entry[2])
    cursor.execute('SELECT * FROM book_user')
    all_user = cursor.fetchall()
    for u in all_user:
        rank[u[0]] = 0
        cursor.execute('SELECT * FROM book_need')
        all_need_2 = cursor.fetchall()
        for entry in all_need_2:
            if entry[3] != userid.id and entry[3] == u[0] and entry[2] in book_list:
                rank[u[0]] += 1
    sorted_rank = sorted(rank, key=rank.get)    ## get sorted user rank
    top_user = sorted_rank[-top_n:]
    rec_books_user_base = []
    for u in top_user:
            cursor.execute('SELECT * FROM book_need')
            need_entry = cursor.fetchall()
            for entry in need_entry:
                if entry[3] != userid and entry[3] == u and entry[2] not in book_list:
                    rec_books_user_base.append(entry[2])
    ## now get the rec books based on similar user
    
    return rec_books_user_base
    
def search_rank():
    global userid
    search_entry = []
    rec_books_search = []
    cursor = connection.cursor()
    print userid.id
    q = 'SELECT entry FROM book_search WHERE user_id = ' + str(userid.id)
    print q
    cursor.execute(q)
    search_entry = cursor.fetchall()
    for e in search_entry:
        rec_books_search.append(entry_search(e))
        
    

def recommended_to_you(request):
    rec_from_user = user_rank()
    search_rank()
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
    major_list_raw = hotness()
    major_list = {}
    for key, value in major_list_raw.items():
        major_list[key] = "{0:.1f}".format(value*1000)
    print major_list
    template = loader.get_template('book/index.html')
    context = RequestContext(request,{
        'major_list' : major_list
    })
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
    global userid        
    if request.method == "POST":
        entry = request.POST.get("keyword",' ')
        if entry == '':
            return redirect(home)
        print entry
        book_list = []
        user_list = []
        is_title=0
        if userid != 1000000:
            Search.objects.create(entry=entry, user=userid)

        for c in entry:
           if ord(c) < 47 or ord(c) > 58:
                is_title = 1
        if not is_title:
            book_list.append(Book.objects.get(ISBN__contains=entry))
        else:
            books = Book.objects.filter(title__contains=entry)
            for b in books:
                book_list.append(b)
        for b in book_list:
            find = 0
            for n in Need.objects.all():
                print n.book == b
                if n.intention == "have" and n.book == b:
                    user_list.append(n.user)
                    find = 1
                    break
                else:
                    continue
            if not find:
                user_list.append(" ")
    book_user = zip(book_list, user_list)
    print book_user
    template = loader.get_template('book/search.html')
    context = RequestContext(request,{
        'keyword' : entry,
        'book_user': book_user
    })
    return HttpResponse(template.render(context))

def search_result(entry):
    book_list = []
    is_title=0 
    if entry == '':
        return []
    for c in entry:
        if ord(c) < 47 or ord(c) > 58:
            is_title = 1
    if not is_title:
        book_list.append(Book.objects.get(ISBN__contains=entry))
    else:
        books = Book.objects.filter(title__contains=entry)
        for b in books:
            book_list.append(b)
    return book_list

def hotness():
    global hotness_dic
    hotness_dic = {"CS":0, "MATH":0, "HIST":0, "CHEM":0}
    searched_book = []
    searched_entry = []
    category_list = []
    threadhold = 100
    for entry in Search.objects.all():
        searched_entry.append(entry.entry)
    print searched_entry
    for e in searched_entry:
        searched_book.append(search_result(e))
    print hotness_dic
    for books in searched_book:
        if len(books) > threadhold:
            books = random.sample(books, threadhold)
        for book in books:
            category_list.append(book.category)
            hotness_dic[book.category] = hotness_dic[book.category] + 1
    major_list = calculate_hotness(hotness_dic)
    print hotness_dic
    print major_list
    return major_list

def major_count(category_list, result):
    for major in category_list:
        if result.get(major) == None:
            result[major] = 1
        else:
            result[major] += 1


def calculate_hotness(result):
    total = 0.0;
    major_list = {}
    for key, value in result.items():
        total += value
    for key, value in result.items():
        major_list[key] = value/total;
    return major_list
