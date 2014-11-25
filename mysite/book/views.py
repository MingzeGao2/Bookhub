from django.shortcuts import render_to_response , render
from django.http import HttpResponse
from book.models import Need, Book, User
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.db import connection

userid = 0;
def needbook (request):
    ISBN = ''
    if request.method == 'POST':
        ISBN = request.POST.get("isbn",' ')    
    try:
        global ISBN
        output = []
        neededBood = Book.objects.raw('SELECT * FROM book_book WHERE ISBN = %s',[ISBN])[0]
        for p in Need.objects.filter(book=neededBood,intention='need'):
            output.append(p.__str__() + ', ')
        output[-1] = output[-1][0:-1]
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
     

def havebook (request):
    if request.method == 'POST':
        ISBN = request.POST.get("isbn", ' ')
    try:
        book = Book.objects.raw('SELECT * FROM book_book WHERE ISBN = %s',[ISBN])[0]
        bookid = book.id
        cursor = connection.cursor()
        cursor.execute('SELECT amount FROM book_book WHERE id = %s',[bookid])
        amount = cursor.fetchone()
        amount = amount[0] + 1
        cursor.execute('UPDATE book_book SET amount = %s WHERE id = %s',[amount,bookid])
        result = Need.objects.filter(book=book, intention = "need")
        output = ', '.join([p.user.__str__() for p in result])
        if output == '':
            return HttpResponse("Sorry, no one is looking for %s" %book.title)
        output += ' need %s' %(book.title)
        output += '......now we have %s %s' %(book.amount, book.title)
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
        
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
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
        
def delete(request):
    template = loader.get_template('book/deletebook.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def insertbook(request):
    if request.method == "POST":
        ISBN = request.POST.get("isbn", ' ')
        Category = request.POST.get("category",' ')
        Title = request.POST.get("title",' ')
        Amount = request.POST.get("amount",' ')
        try:
            book = Book.objects.get(ISBN=ISBN)
        except ObjectDoesNotExist:
            try:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO book_book (ISBN, category, title, amount) VALUES(%s, %s, %s, %s)',[ISBN, Category, Title, Amount])
            except :
                return HttpResponse("%s can't be added to books. " %Title)
            else:
                return HttpResponse("Added %s to database. " %Title)
        else:
            return HttpResponse("%s is already in database." %Title)
        

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

def index(request):
    template = loader.get_template('book/index.html')
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
                
def recommend(request):
    
            
