from django.urls import path
from . import views

urlpatterns = [
    path('adicionar_usuario/', views.adicionar_usuario),
]
