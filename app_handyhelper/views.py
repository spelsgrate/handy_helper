from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def register(request):
    print(request.POST)
    errors = User.objects.isRegValid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        passwordFromForm = request.POST['password']
        hashed_password = bcrypt.hashpw(passwordFromForm.encode(), bcrypt.gensalt())
        newuser = User.objects.create(username= request.POST['username'], password=hashed_password.decode())
        print(newuser)
        request.session['userid'] = newuser.id
        return redirect("/dashboard")

def login(request):
    user = User.objects.filter(username=request.POST['username'])
    errors = User.objects.isLoginValid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id

            return redirect('/dashboard')
    return redirect("/")

def display(request):
    print(request.POST)
    id = request.session['userid']
    isSaved = Jobs.objects.filter(saved_jobs=id)
    notSaved = Jobs.objects.exclude(saved_jobs=id)
    context = {
        'isSaved':isSaved,
        'notSaved':notSaved,
    }
    return render(request, 'dashboard.html', context)

def addJob(request):
    return render(request, 'add_job.html')

def addJobSubmit(request):
    print(request.POST)

    errors = Jobs.objects.isJobValid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/addjob")
    else:
        newjob = Jobs.objects.create(title = request.POST['title'], desc=request.POST['desc'], location=request.POST['location'], posted_by=User.objects.get(id=request.session['userid']))
        print(newjob)
        return redirect("/dashboard")

def editJob(request, id):
    job = Jobs.objects.get(id=id)
    context = {
        "job": job
    }
    return render(request, 'edit_job.html', context)

def editJobSubmit(request, id):
    print(request.POST)

    errors = Jobs.objects.isJobValid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/edit/"+str(id))
    else:
        c = Jobs.objects.get(id=id)
        c.title = request.POST['title']
        c.desc = request.POST['desc']
        c.location = request.POST['location']
        c.save()
    return redirect('/dashboard')

def viewJobs(request, id):
    job = Jobs.objects.get(id=id)
    context = {
        "job":job,
    }
    return render(request, "view_job.html", context)

def saveJob(request, id):
    saveJob = Jobs.objects.get(id=id)
    loggedUser = User.objects.get(id=request.session['userid'])
    loggedUser.user_saved_jobs.add(saveJob)
    return redirect('/dashboard')

def cancelJob(request, id):
    canceljob = Jobs.objects.get(id=id)
    loggedUser = User.objects.get(id=request.session['userid'])
    loggedUser.user_saved_jobs.remove(canceljob)
    return redirect('/dashboard')

def delJob(request, id):
    c = Jobs.objects.get(id=id)
    c.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect("/")
