from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('module/', views.ModuleView.as_view(), name='modules')
]
