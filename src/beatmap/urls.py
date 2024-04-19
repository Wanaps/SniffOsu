from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_best/', views.get_best_form, name='get_best_form'),
    path('get_best/<int:beatmapid>', views.get_best, name='get_best'),
    path('get_best_from/', views.get_best_from_form, name='get_best_from_form'),
    path('get_best_from/<str:player>/', views.get_best_from, name='get_best_from'),
    path('compare_score/', views.compare_score_form, name='compare_score_form'),
    path('compare_score/<int:beatmapid>/<str:player1>/<str:player2>', views.compare_score, name='compare_score'),
]