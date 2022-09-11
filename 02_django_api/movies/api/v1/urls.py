from django.urls import path, re_path

from . import views

urlpatterns = (
    path('movies/<str:pk>/', views.MoviesDetailApi.as_view()),
    path('movies/', views.MoviesListApi.as_view()),
)
