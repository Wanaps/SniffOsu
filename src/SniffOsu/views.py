from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return HttpResponseRedirect('home/')