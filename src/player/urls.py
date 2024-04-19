from django.urls import path
from player import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compare/', views.compare_form, name='compare_form'),
    path('compare/<str:username>/<str:username2>', views.compare, name='compare'),
    path ('profile/', views.profile_form, name='profile_form'),
    path ('profile/<str:username>', views.get_user, name='get_user')
]