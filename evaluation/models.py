from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Job(models.Model):
    salary = models.IntegerField()
    title = models.CharField(max_length=20)

class Person(User):
    employeeId = models.IntegerField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)


class PersonCatalog(SingletonModel):
    def addPerson(self, first_name, last_name, password, employeeId):
        job=EmployeeCatalog.load().addEmployee()
        person = Person.objects.create(first_name=first_name, last_name=last_name, password=password,
                                       employeeId=employeeId,job=job)
        return person

    def editPerson(self, employeeId, password):
        person = Person.objects.get(employeeId=employeeId)
        person.password = password
        person.save()

    def deletePerson(self, employeeId):
        Person.objects.get(employeeId=employeeId).delete()

    def showPerson(self):
        return Person.objects.all()


class PersonFormRegister(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'employeeId', 'password',)


class PersonFormEdit(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('employeeId', 'password',)


class PersonFormDelete(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('employeeId',)





class Employee(Job):
    title = 'Employee'
    salary = 1000


class EmployeeCatalog(SingletonModel):

    def addEmployee(self):
        employee = Employee.objects.create()
        return employee