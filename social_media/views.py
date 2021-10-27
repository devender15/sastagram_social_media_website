from django.urls import path, include
from django.shortcuts import redirect

def home(req):
	return redirect("/users/login")