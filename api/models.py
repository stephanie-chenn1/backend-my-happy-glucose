from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(null=False)
    email = models.EmailField(max_length=250)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Meal(models.Model):
    qty = models.IntegerField(null=False)
    unit = models.CharField(max_length=10)
    food = models.CharField(max_length=50)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    carb_count = models.IntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.carb_count
    
    def to_json(self):
        return {
            "id": self.id,
            "qty": self.qty,
            "unit": self.unit,
            "food": self.food,
            "date": self.date,
            "time": self.time,
            "carb_count": self.carb_count,
            "user": self.user.id
        }

class Glucose(models.Model):
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    glucose = models.IntegerField(null=False)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.glucose_level

class Fitness(models.Model):
    date = models.DateField(null=False)
    duration = models.IntegerField(null=False)
    workout_type = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.workout_type

