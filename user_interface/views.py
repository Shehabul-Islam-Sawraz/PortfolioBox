from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from .models import (User,InformationModel,EducationModel,ExperienceModel,ProjectModel,MessageModel,SkillsetModel)

# Create your views here.

def index(request):
    return render(request, template_name="user_interface/index.html")
    # return HttpResponse("Hello, world. You're at the polls index.")

def login_view(request, *args, **kwargs):
    if request.method == "POST":
        # User trying to log in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Checking if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "user_interface/login.html", {"message": "Invalid Username or Password!! Please check again.."})
    
    else:
        return render(request, "user_interface/login.html", {"message": ""})    
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"] 
        
        # Checking password match
        password = request.POST["password"]
        confirmationPass = request.POST["confirmation"]
        
        if password!=confirmationPass:
            return render(request, "user_interface/register.html", {"message": "Password doesn't match!! Please enter again.."})
        
        #Create new user if passwords matches
        
        try:
            user = User.objects.create_user(username,email,password)
            user.save()
        except IntegrityError:
            return render(request, "user_interface/register.html", {"message": "Username already exists.."})
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "user_interface/register.html")