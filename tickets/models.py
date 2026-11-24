from django.db import models
class Ticket(models.Model):
    title=models.CharField('Тақырып',max_length=200)
    description=models.TextField('Сипаттама')
    priority=models.CharField('Басымдық',max_length=20,choices=[('low','Төмен'),('normal','Орташа'),('high','Жоғары')],default='normal')
    status=models.CharField('Мәртебе',max_length=20,default='Жаңа')

import uuid
class Service(models.Model):
    name=models.CharField(max_length=120)
    detail=models.TextField()
    price=models.PositiveIntegerField()
    def __str__(self): return self.name

class Request(models.Model):
    code=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=40)
    address=models.CharField(max_length=250,blank=True)
    service=models.ForeignKey(Service,on_delete=models.PROTECT)
    title=models.CharField(max_length=200)
    description=models.TextField(max_length=2000)
    priority=models.CharField(max_length=20,choices=[('normal','Обычный'),('high','Срочный')],default='normal')
    status=models.CharField(max_length=20,choices=[('new','Жаңа / Новая'),('work','В работе'),('done','Выполнена')],default='new')
    created=models.DateTimeField(auto_now_add=True)
class Review(models.Model):
    name=models.CharField(max_length=80)
    text=models.TextField(max_length=1000)
    approved=models.BooleanField(default=False)
class Chat(models.Model):
    message=models.TextField(max_length=500)
    answer=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
