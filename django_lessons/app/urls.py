from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('subjects/', views.SubjectsListView.as_view(), name='subjects'),
    path('modules/<int:subject_id>/', views.ModulesListView.as_view(), name='modules'),
    path('exercises/<int:module_id>/', views.ExerciseListView.as_view(), name='exercises'),
    path(r'^exercises/(?P<pk>\d+)/$', views.ExerciseDetailView.as_view(), name='exercise')
]
