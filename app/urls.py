
from django.urls import path
from .views import home, Periodic
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('Periodic', views.Periodic, name="Periodic"),
    path('Event', views.Event, name="Event"),
    path('PGP', views.PGP, name="PGP"),
    path('HEI', views.HEI, name="HEI"),
    path('ResearchInstitution', views.Research, name="ResearchInstitution"),
    path('Geographic', views.Geographic, name="Geographic")
]

