import random
userid = 1000000
hotness = {"CS":0, "MATH":0, "HIST":0, "CHEM":0}

def hotness(request):
    global hotness
    searched_book = []
    searched_entry = []
    category_list = []
    threadhold = 100
    for entry in Search.objects.all():
        searched_entry.append(entry.entry)
    for e in searched_entry:
        searched_book.append(search_result(e))
    for books in searched_book:
        if len(books) > threadhold:
            books = random.sample(books, threadhold)
        print books
        for book in books:
            category_list.append(book.category)
            hotness[book.category] += 1
