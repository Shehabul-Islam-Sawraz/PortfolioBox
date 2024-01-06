from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from .models import (User, InformationModel, EducationModel, ExperienceModel,ProjectModel,MessageModel,SkillsetModel)
from .forms import (IntroForm, EducationForm, ExperienceForm, ProjectForm,MessageForm,SkillsetForm,ContactForm)
from django.contrib.auth.decorators import login_required
from .serializers import (userSerializer, informationSerializer, educationSerializer, experienceSerializer, projectSerializer, skillsetSerializer, messageSerializer)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import serializers, permissions
from django.core.mail import send_mail, BadHeaderError

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

@api_view(['GET'])
@permission_classes((permissions.AllowAny, permissions.IsAuthenticated))
def api_view(request, username, *args, **kwargs):
    bioProfile = User.objects.get(username = username)
    information_qs = InformationModel.objects.filter(user = bioProfile).first()
    education_qs = EducationModel.objects.filter(user = bioProfile).all()
    experience_qs = ExperienceModel.objects.filter(user = bioProfile).all()
    project_qs = ProjectModel.objects.filter(user = bioProfile).all()
    skillset_qs = SkillsetModel.objects.filter(user = bioProfile).all()
    message_qs = MessageModel.objects.filter(user = bioProfile).all()
    messageform_qs = MessageForm()
    #Calling Serializers
    username_serializer = userSerializer(bioProfile, many=False)
    information_serializer = informationSerializer(information_qs, many=False)
    education_serializer = educationSerializer(education_qs, many=True)
    experience_serializer = experienceSerializer(experience_qs, many=True)
    project_serializer = projectSerializer(project_qs, many=True)
    skillset_serializer = skillsetSerializer(skillset_qs, many=True)
    message_serializer = messageSerializer(message_qs, many=True)
    context = {
        "username": username,
        "user": username_serializer.data,
        "information": information_serializer.data,
        "education": education_serializer.data,
        "experience": experience_serializer.data,
        "projects": project_serializer.data,
        "skillsets": skillset_serializer.data,
        # "message_form": messageform_qs.data,
    }
    return Response(context)


def portfolio_view(request, username, *args, **kwargs):
    template_name = 'user_interface/portfolio.html'
    context = {}
    userprofile = get_object_or_404(User, username = username)

    # try:
    #     userprofile = User.objects.get(username = username)
    # except User.DoesNotExist:
    #     raise Http404('User does not exists.  Please Provide User Information First')

    bioProfile = User.objects.get(username = username)
    information_qs = InformationModel.objects.filter(user = bioProfile).first()
    education_qs = EducationModel.objects.filter(user = bioProfile).all()
    experience_qs = ExperienceModel.objects.filter(user = bioProfile).all()
    project_qs = ProjectModel.objects.filter(user = bioProfile).all()
    skillset_qs = SkillsetModel.objects.filter(user = bioProfile).all()
    message_qs = MessageModel.objects.filter(user = bioProfile).all()
    messageform_qs = MessageForm()
    #Calling Serializers
    username_serializer = userSerializer(bioProfile, many=False)
    information_serializer = informationSerializer(information_qs, many=False)
    education_serializer = educationSerializer(education_qs, many=True)
    experience_serializer = experienceSerializer(experience_qs, many=True)
    project_serializer = projectSerializer(project_qs, many=True)
    skillset_serializer = skillsetSerializer(skillset_qs, many=True)
    message_serializer = messageSerializer(message_qs, many=True)

    if request.method == "GET":
        print('GET Method')
        form = ContactForm()
        context = {
            "username": username,
            "user": username_serializer.data,
            "information": information_serializer.data,
            "education": education_serializer.data,
            "experience": experience_serializer.data,
            "projects": project_serializer.data,
            "skillsets": skillset_serializer.data,
            # "message_form": messageform_qs.data,
            "form": form.data,
        }
    else:
        print('POST Method')
        to_email = information_qs.email
        print(f'To EMAIL of portfolio user. ---> {to_email}')
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            new_subject = 'Sender: ' + name + ' Subject:' + subject
            # print(name, from_email, new_subject, message)
            try:
                send_mail(new_subject, message, from_email, [to_email, 'admin@gmail.com'])
                form_message = "Thank You for connecting with us. Your message has been received!" 
            except BadHeaderError:
                form_message = "There was a bad header error. Please try again!!" 
                # return HttpResponseRedirect(reverse("portfolio"))
                return redirect('portfolio')
        # COntact form works
        context = {
            "username": username,
            "user": username_serializer.data,
            "information": information_serializer.data,
            "education": education_serializer.data,
            "experience": experience_serializer.data,
            "projects": project_serializer.data,
            "skillsets": skillset_serializer.data,
            "form": form,
            "form_message": form_message,
        }
    
    return render(request, template_name, context)
