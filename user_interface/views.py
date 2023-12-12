from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from .models import (User,InformationModel,EducationModel,ExperienceModel,ProjectModel,MessageModel,SkillsetModel)
from .forms import (IntroForm,EducationForm,ExperienceForm,ProjectForm,MessageForm,SkillsetForm,ContactForm)
from django.contrib.auth.decorators import login_required
from .serializers import (userSerializer, informationSerializer, educationSerializer, experienceSerializer, projectSerializer, skillsetSerializer, messageSerializer)

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
            return HttpResponseRedirect(reverse("create"))
        else:
            return render(request, "user_interface/loginRegister.html", {"message": "Invalid Username or Password!! Please check again.."})
    
    else:
        return render(request, "user_interface/loginRegister.html", {"message": ""})    
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"] 
        
        # Checking password match
        password = request.POST["password"]
        confirmationPass = request.POST["confirmation"]
        
        if password!=confirmationPass:
            return render(request, "user_interface/loginRegister.html", {"message": "Password doesn't match!! Please enter again.."})
        
        # Create new user if passwords matches
        try:
            user = User.objects.create_user(username,email,password)
            user.save()
        except IntegrityError:
            return render(request, "user_interface/loginRegister.html", {"message": "Username already exists.."})
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "user_interface/loginRegister.html")
    
@login_required(login_url='login')
def form_createView(request, *args, **kwargs):
    template_name = 'user_interface/create.html'
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    intro_form = IntroForm(request.POST or None)
    if intro_form.is_valid():
        intro_form.save(commit = False)
        intro_form.user = user
        intro_form.save(request = request)
    else:
        intro_form = IntroForm()

    edu_form = EducationForm(request.POST or None)
    if edu_form.is_valid():
        edu_form.save(commit=False)
        edu_form.user = user
        edu_form.save(request = request)
    else:
        edu_form = EducationForm()

    exp_form = ExperienceForm(request.POST or None)
    if exp_form.is_valid():
        exp_form.save(commit=False)
        exp_form.user = user
        exp_form.save(request = request)
    else:
        exp_form = ExperienceForm()

    project_form = ProjectForm(request.POST or None)
    if project_form.is_valid():
        project_form.save(commit=False)
        project_form.user = user
        project_form.save(request = request)
    else:
        project_form = ProjectForm()
    
    skill_form = SkillsetForm(request.POST or None)
    if skill_form.is_valid():
        skill_form.save(commit=False)
        skill_form.user = user
        skill_form.save(request = request)
    else:
        skill_form = SkillsetForm()

    context = {
        'user': user,
        'introFORM': IntroForm(),
        'eduFORM': EducationForm(),
        'expFORM': ExperienceForm(),
        'projectFORM': ProjectForm(),
        'skillFORM': SkillsetForm(), # skill_form,
    }

    return render(request, template_name, context)

# Information Form View
@login_required(login_url='login')
def introForm_createView(request, *args, **kwargs):
    template_name = 'user_interface/information_create.html'
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"
        
    if request.method == 'POST':
        intro_form = IntroForm(request.POST or None)
        if intro_form.is_valid():
            intro_form.save(commit = False)
            intro_form.user = user
            intro_form.save(request = request)
    else:
        intro_form = IntroForm()
    context = {
        'user': user,
        'introFORM': IntroForm(),
    }
    return render(request, template_name, context)

# Education Form View
@login_required(login_url='login')
def eduForm_createView(request, *args, **kwargs):
    template_name = 'user_interface/education_create.html'
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"
        
    bioProfile = User.objects.get(username = user)
    education_qs = EducationModel.objects.filter(user = bioProfile).all()
    education_serializer = educationSerializer(education_qs, many=True)

    if request.method == 'POST':
        edu_form = EducationForm(request.POST or None)
        if edu_form.is_valid():
            edu_form.save(commit=False)
            edu_form.user = user
            edu_form.save(request = request)
    else:
        edu_form = EducationForm()
    context = {
        'user': user,
        'eduFORM': EducationForm(),
        "education": education_serializer.data,
    }
    return render(request, template_name, context)

# Experiece Form View
@login_required(login_url='login')
def expForm_createView(request, *args, **kwargs):
    template_name = 'user_interface/experience_create.html'
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"
        
    bioProfile = User.objects.get(username = user)
    experience_qs = ExperienceModel.objects.filter(user = bioProfile).all()
    experience_serializer = experienceSerializer(experience_qs, many=True)
    if request.method == 'POST':
        exp_form = ExperienceForm(request.POST or None)
        if exp_form.is_valid():
            exp_form.save(commit=False)
            exp_form.user = user
            exp_form.save(request = request)
    else:
        exp_form = ExperienceForm()
    context = {
        'user': user,
        'expFORM': ExperienceForm(),
        "experience": experience_serializer.data,
    }
    return render(request, template_name, context)

# Project Form View
@login_required(login_url='login')
def projectForm_createView(request, *args, **kwargs):
    template_name = 'user_interface/project_create.html'
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"
        
    bioProfile = User.objects.get(username = user)
    project_qs = ProjectModel.objects.filter(user = bioProfile).all()
    project_serializer = projectSerializer(project_qs, many=True)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST or None)
        if project_form.is_valid():
            project_form.save(commit=False)
            project_form.user = user
            project_form.save(request = request)
    else:
        project_form = ProjectForm()
    context = {
        'user': user,
        'projectFORM': ProjectForm(),
        "projects": project_serializer.data,
    }
    return render(request, template_name, context)



# Skillset Form View
@login_required(login_url='login')
def skillForm_createView(request, *args, **kwargs):
    template_name = 'user_interface/skill_create.html'
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"
        
    bioProfile = User.objects.get(username = user)
    skillset_qs = SkillsetModel.objects.filter(user = bioProfile).all()
    skillset_serializer = skillsetSerializer(skillset_qs, many=True)

    if request.method == 'POST':
        skill_form = SkillsetForm(request.POST or None)
        if skill_form.is_valid():
            skill_form.save(commit=False)
            skill_form.user = user
            skill_form.save(request = request)
    else:
        skill_form = SkillsetForm()

    context = {
        'user': user,
        'skillFORM': SkillsetForm(), # skill_form,
        "skillsets": skillset_serializer.data,
    }
    return render(request, template_name, context)