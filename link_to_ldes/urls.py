from django.urls import path
from . import views

urlpatterns = [
	path('getlink/', views.getlink),
    path('contact', views.contact),
]
