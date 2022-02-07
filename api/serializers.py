from rest_framework import serializers
from .models import User, Meal, Glucose

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'age', 'email', 'username')

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'qty', 'unit', 'food', 'date', 'time', 'user', 'carb_count')

class GlucoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glucose
        fields = ('id', 'date', 'time', 'glucose', 'notes', 'user')
