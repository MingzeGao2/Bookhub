from django.shortcuts import render_to_response , render
from django.http import HttpResponse
from book.models import Need, Book
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
def needbook (request):
    if request.method == 'POST':
        ISBN = request.POST.get("isbn",' ')    
    try:
        book = Book.objects.get(ISBN=ISBN)
        result = Need.objects.filter(book=book,intention = "have")
        output = ', '.join([p.__str__() for p in result])
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
     

def havebook (request):
    if request.method == 'POST':
        ISBN = request.POST.get("isbn", ' ')
    try:
        book = Book.objects.get(ISBN=ISBN)
        book.amount +=1
        book.save()
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
        book = Book.objects.get(ISBN=ISBN)
        title = book.title
        book.delete()
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
            newbook= Book.objects.create(ISBN=ISBN, category=Category, amount=Amount, title=Title)
            newbook.save()
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
