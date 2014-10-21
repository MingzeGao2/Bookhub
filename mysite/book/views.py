from django.shortcuts import render_to_response , render
from django.http import HttpResponse
from book.models import Need, Book
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
def need (request, ISBN):
    try:
        book = Book.objects.get(ISBN=ISBN)
        result = Need.objects.filter(book=book,intention = "have")
        output = ', '.join([p.__str__() for p in result])
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
     

def have (request, ISBN):
    try:
        book = Book.objects.get(ISBN=ISBN)
        book.amount +=1
        book.save()
        result = Need.objects.filter(book=book, intention = "need")
        output = ', '.join([p.user.__str__() for p in result])
        output += ' need %s' %(book.title)
        output += '......now we have %s %s' %(book.amount, book.title)
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
        
def delete(request, ISBN):
    try:
        book = Book.objects.get(ISBN=ISBN)
        title = book.title
        book.delete()
        output = "%s has been deleted."%(title)
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
    

def insertbook(request, ISBN, Category, Amount, Title):
    try:
        book = Book.objects.get(ISBN=ISBN)
    except ObjectDoesNotExist:
        try:
            newbook= Book.objects.create(ISBN=ISBN, category=Category, amount=Amount, title=Title)
            newbook.save()
        except :
            return HttpResponse("%s can't be added to books." %Title)
        else:
            return HttpResponse("Added %s to database." %Title)
    else:
        return HttpResponse("%s is already in database." %Title)
        
##def Register(request):
##    if request.method == "POST":
##        ISBN = request.POST.get("isbn", '')
##    return HttpResponse("%s" ISBN)
##        
def index(request):
    template = loader.get_template('book/index.html')
    return HttpResponse(template)
