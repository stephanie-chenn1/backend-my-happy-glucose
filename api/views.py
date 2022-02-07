from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import generics, status
from .serializers import MealSerializer, UserSerializer, GlucoseSerializer
from .models import User, Meal, Glucose
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
import requests
import os                                                                                                                                                                                                          

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MealView(APIView):
    def get(self, request, user_id=None, **kwargs):
        try:
            queryset = Meal.objects.all()
            date = request.query_params["date"]
            if date != None:
                meals = queryset.filter(date=date, user=user_id)
                if not meals:
                    return Response({"Details": "No meals for this date"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    serializer = MealSerializer(meals, many=True) 
    
        except:
            queryset = Meal.objects.all()
            if user_id is not None:
                meals = queryset.filter(user=user_id)
            else:
                meals = queryset
            serializer = MealSerializer(meals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id=None, format=None):
        if "id" in request.data and "date" in request.data and "user" in request.data:
            try:
                id = self.request.data.get("id")
                date = self.request.data.get("date")
                user= self.request.data.get("user")
                
                meal = Meal.objects.get(id=id,date=date, user=user)
                meal.delete()
                return Response({"Details": f"Successfully deleted meal id {id}"}, status=status.HTTP_200_OK)
            except Meal.DoesNotExist:
                return Response({"Details": "Meal does not exist in db"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Details": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_id= None, format=None):

        if "qty" in request.data and "unit" in request.data and "food" in request.data and "time" in request.data and "user" in request.data and "date" in request.data and user_id is not None:
            food = self.request.data.get("food")
            # Ingredient search
            url_1 = "https://api.spoonacular.com/food/ingredients/search"
            apiKey = str(os.getenv("API_KEY"))
            params_1 = {"query": food, "apiKey": apiKey}
            r_1 = requests.get(url = url_1, params = params_1)
            if r_1.status_code != 200:
                return Response("Details: Missing food parameter", status.HTTP_400_BAD_REQUEST)
            else:
                data_1 = r_1.json()
                food_id = data_1["results"][0]["id"]
                
                # Get nutrient by ingredident id
                url_2 = f"https://api.spoonacular.com/food/ingredients/{food_id}/information"
                amt = self.request.data.get("qty")
                unit = self.request.data.get("unit")
                params_2 = {"id": food_id, "amount": amt, "unit": unit, "apiKey":apiKey}
                r_2 = requests.get(url = url_2, params=params_2)

                if r_2.status_code != 200:
                    return Response("Api request 2 was unsuccessful")
                else:
                    final_data = r_2.json()
                    carb_count = final_data["nutrition"]["nutrients"][9]["amount"]
                    meal_data = Meal(
                        qty= amt,
                        unit= unit,
                        food= food,
                        time= self.request.data.get("time",None),
                        date= self.request.data.get("date",None),
                        carb_count= carb_count,
                        user= User.objects.get(pk=self.request.data.get("user"))
                        )
                    meal_data.save()
                    return Response(meal_data.to_json(), status=status.HTTP_201_CREATED)

        else:
            return Response({"Details": "Missing params in request body"}, status=status.HTTP_400_BAD_REQUEST)
        

class GlucoseView(APIView):

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"Details": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Glucose.objects.all()
        glucose = queryset.filter(user=user_id)

        serializer = GlucoseSerializer(glucose, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"Details": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GlucoseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    