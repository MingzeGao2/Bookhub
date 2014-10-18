from django.contrib import admin
from book.models import User, Book, Need, Course, Require, Registration
# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Need)
admin.site.register(Course)
admin.site.register(Require)
admin.site.register(Registration)
