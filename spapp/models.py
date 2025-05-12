from django.db import models

# Create your models here.
class Collection(models.Model):
    Phase_Choice=[
        ('Phase I','Phase I'),
        ('Phase II','Phase II'),
        ('Phase III','Phase III'),
        ('Phase IV','Phase IV'),
    ]
    Study_Name=models.CharField(max_length=100)
    Study_Description=models.TextField()
    Study_Phase=models.CharField(max_length=100, choices=Phase_Choice)
    Sponser_Name=models.CharField(max_length=100)
    
    class Meta:
        db_table='datas'