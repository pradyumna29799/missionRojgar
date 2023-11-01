from django.urls import path
from . import views

urlpatterns = [
    
    path('index', views.index, name='index'),
    path('candidate', views.candidate, name='candidate'),
    path('employee', views.employee, name='employee'),
    path('first_floor', views.first_floor, name='first_floor'),
    path('second_floor', views.second_floor, name='second_floor'),
    path('third_floor', views.third_floor, name='third_floor'),
    path('fourth_floor', views.fourth_floor, name='fourth_floor'),
    path('notifyButton', views.notifyButton, name='notifyButton'),
    path('screen', views.screen, name='screen')
    
]