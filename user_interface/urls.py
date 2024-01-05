from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('create', views.form_createView, name='create'),
    path("create/information", views.introForm_createView, name='information'),
    path("create/education", views.eduForm_createView, name='education'),
    path("create/experience", views.expForm_createView, name='experience'),
    path("create/project", views.projectForm_createView, name='project'),
    path("create/skillset", views.skillForm_createView, name='skillset'),
    path("api/<str:username>", views.api_view, name='api'),
    path("<str:username>", views.portfolio_view, name='portfolio'),
]