from django.shortcuts import render_to_response 
from django.http import HttpResponse
from book.models import Need, Book
from django.core.exceptions import ObjectDoesNotExist
def need (request, ISBN):
    try:
        book = Book.objects.get(ISBN=ISBN)
        result = Need.objects.filter(book=book,intention = "have")
        output = ', '.join([p.__str__() for p in result])
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, we don't have this book")
    else:
        return HttpResponse(output)
  ##  else:
##        return HttpResponse("Sorry, we don't have this book.")
     

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
    
