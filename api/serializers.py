from rest_framework import serializers
from .models import User, Meal, Glucose, Fitness, Mood

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'age', 'email', 'username', 'password')

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'qty', 'unit', 'food', 'date', 'time', 'user', 'carb_count')

class GlucoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glucose
        fields = ('id', 'date', 'time', 'glucose', 'notes', 'user')

class FitnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fitness
        fields = ('id', 'date', 'duration', 'workout_type', 'notes', 'user')

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ('id', 'date', 'time', 'mood', 'user')
