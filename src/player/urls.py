from django.urls import path
from player import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compare/', views.compare_form, name='compare_form'),
    path('compare/<str:username>/<str:username2>', views.compare, name='compare'),
    path ('<str:username>/', views.get_user, name='get_user'),
    # path ('<player>/', views.detail, name='detail'),
    # path ('<player>/compare/', views.compare, name='compare')
]