from django.db import models

# Create your models here.

class Departments(models.Model):
    DepartmentId = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=100)
    summ = models.CharField(max_length=100000,default="null")
    output = models.CharField(max_length=100000,default="null")

class Employees(models.Model):
    EmployeeId = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=100,default="null")
    Department = models.CharField(max_length=100,default="null")
    DateOfJoining = models.DateField()
    PhotoFileName = models.CharField(max_length=100,default="null")
    AudioFileName = models.CharField(max_length=100,default="null")
    AudioText = models.CharField(max_length=1000000,default="null")
    AudioSummary = models.CharField(max_length=1000000,default="null")

