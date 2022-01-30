from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('subjects/', views.SubjectsListView.as_view(), name='subjects'),
    path('favorites/<int:pk>/', views.FavoritesListView.as_view(), name='favorites'),
    path('modules/<int:subject_id>/',
         views.ModulesListView.as_view(), name='modules'),
    path('modules/<int:module_id>/exercises/',
         views.ExerciseListView.as_view(), name='exercises'),
    path('modules/<int:module_id>/exercises/<int:pk>',
         views.ExerciseDetailView.as_view(), name='exercise')
]
