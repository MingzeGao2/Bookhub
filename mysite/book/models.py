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
        return self.ISBN
    ISBN = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)

class Need(models.Model):
    def __str__(self):
        return self.user + ' '+self.intention+' '+ self.book
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
        return self.course + ' requires ' + self.required_book
    course = models.ForeignKey(Course)
    required_book = models.ForeignKey(Book)

class Registration(models.Model):
    def __str__(self):
        return self.student + ' register ' + self.to_course
    student = models.ForeignKey(User)
    to_course = models.ForeignKey(Course)

