from django.db import models

# Create your models here.

class User(models.Model):
    def __str__(self):
        return self.netid
    User_name = models.CharField(max_length=200)
    major = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    netid = models.CharField(max_length=200)

class Book(models.Model):
    def __str__(self):
        return self.title 
    ISBN = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)

class Need(models.Model):
    def __str__(self):
        return self.user.__str__() + ' '+self.intention+' '+ self.book.title
    intention = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)

class Course(models.Model):
    def __str__(self):
        return self.semester + ' ' + self.course_title
    course_title = models.CharField(max_length=200)
    semester = models.CharField(max_length=200)
    
class Require(models.Model):
    def __str__(self):
        return self.course.__str__() + ' requires ' + self.required_book.__str__()
    course = models.ForeignKey(Course)
    required_book = models.ForeignKey(Book)

class Registration(models.Model):
    def __str__(self):
        return self.student.__str__() + ' register ' + self.to_course.__str__()
    student = models.ForeignKey(User)
    to_course = models.ForeignKey(Course)

