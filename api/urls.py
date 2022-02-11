from django.urls import path
from .views import UserView, MealView, GlucoseView, FitnessView, LoginView
from rest_framework import routers


urlpatterns = [
    path('users', UserView.as_view()),
    path('users/<int:user_id>', LoginView.as_view()),
    path('users/<int:user_id>/meals',MealView.as_view()),
    path('users/<int:user_id>/glucose',GlucoseView.as_view()),
    path('users/<int:user_id>/fitness',FitnessView.as_view()),
    # path('get-user', GetUser.as_view()),
    path('meals', MealView.as_view()),
    # path('meals/<int:id>', MealView.as_view())
    # path('add-meal', AddMealView.as_view())
]
