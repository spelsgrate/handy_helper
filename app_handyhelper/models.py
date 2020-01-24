from django.db import models
from django.db.models import Model
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
    #appends to errors{}
    def isRegValid(self, postData):
        errors = {}
        userWithUsernames = User.objects.filter(username=postData['username'])
        if len(postData['username'])<1:
            errors['username'] = "You must enter something"
        if len(userWithUsernames)>0:
            errors['username'] = "You must enter a unique name"
        if len(postData['password']) <8:
            errors['password'] = "You must enter password of at least 8 characters"
        if postData['password'] !=postData['confirm_password']:
            errors['confirm_password']= "Passwords must match"
        
        return errors

    def isLoginValid(self, postData):
        errors = {}
        if len(postData['username'])<3:
            errors['username']= "Your username must be at least 3 charecters"
        user=User.objects.filter(username=postData['username'])
        if len(user)==0:
            errors['username']="This username does not exist"
        else:
            print(user)
            user=user[0]
            print(user)
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("password match")
            else:
                print("failed password")
                errors["passwordwrong"] ="invalid password"
        print(errors)
        return errors

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=96)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class JobsManager(models.Manager):
    def isJobValid(self, postData):
        errors = {}
        if len(postData['title'])<3:
            errors['title'] = "the title is too short"
        if len(postData["desc"])<10:
            errors["desc"] = "The description needs to be at least 10 characters"
        if len(postData["location"])<6:
            errors["location"] = "The location needs to be at least 6 characters"
        return errors

class Jobs(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    location = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="user_posted_by", on_delete=models.CASCADE)
    saved_jobs = models.ManyToManyField(User, related_name="user_saved_jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobsManager()