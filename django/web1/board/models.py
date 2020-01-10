from django.db import models

class Table1(models.Model):
    objects = models.Manager() #vs code 오류 제거용

    no      = models.AutoField(primary_key=True)
    title   = models.CharField(max_length=200)
    content = models.TextField()
    writer  = models.CharField(max_length=50)
    hit     = models.IntegerField()
    img     = models.BinaryField(null=True) 
    regdate = models.DateTimeField(auto_now_add=True)


class Table2(models.Model):
    objects = models.Manager() #vs code 오류 제거용

    no       = models.AutoField(primary_key=True)
    name     = models.CharField(max_length=30)
    kor      = models.TextField()
    eng      = models.TextField()
    math     = models.TextField()
    regdate  = models.DateTimeField(auto_now_add=True)