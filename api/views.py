from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import generics, status
from .serializers import MealSerializer, UserSerializer
from .models import User, Meal
from rest_framework.views import APIView
from rest_framework.response import Response
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

    def post(self, request, user_id= None, format=None):
        # serializer = MealSerializer(data=request.data)

        if "qty" in request.data and "unit" in request.data and "food" in request.data and "time" in request.data and "user" in request.data and user_id is not None:
            food = self.request.data.get("food")
            # Ingredient search
            url_1 = "https://api.spoonacular.com/food/ingredients/search"
            apiKey = str(os.getenv("API_KEY"))
            params_1 = {"query": food, "apiKey": apiKey}
            r_1 = requests.get(url = url_1, params = params_1)
            if r_1.status_code != 200:
                return Response("Api request 1 was not successful")
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
                        carb_count= carb_count,
                        user= User.objects.get(pk=self.request.data.get("user"))
                        )
                    meal_data.save()
                    return Response(f"Meal was successfully saved, carb_count is {carb_count}", status=status.HTTP_201_CREATED)
        else:
            return Response({"Bad request": "Missing params in request body"}, status=status.HTTP_400_BAD_REQUEST)
        



# class GetUser(APIView):
#     serializer_class = UserSerializer
#     lookup_url_kwarg = 'username'

#     def get(self, request, format=None):
#         username= request.GET.get(self.lookup_url_kwarg)
#         if username != None:
#             user = User.objects.filter(username=username)
#             if len(user) > 0:
#                 data = UserSerializer(user[0]).data
#                 return Response(data, status=status.HTTP_200_OK)
#             else:
#                 return Response({'User not found': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)
#         return Response({'Bad request': 'User id parameter not found'}, status=status.HTTP_400_BAD_REQUEST)


# class AddMealView(APIView):
#     serializer_class = AddMealSerializer
#     lookup_url_kwarg = 'user_id'

#     def post(self, request, format=None):
#         id = request.GET.get(self.lookup_url_kwarg)

#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             qty = serializer.data.get('qty')
#             unit = serializer.data.get('unit')
#             food = serializer.data.get('food')
#             date = serializer.data.get('date')
#             time = serializer.data.get('time')
#             carb_count = serializer.data.get('carb_count')
#             # user = serializer.data.get('user')
            
#             meal = Meal(qty=qty, unit=unit, food=food, date=date, time=time, carb_count=carb_count, username=username)
#             meal.save()
#         return Response(AddMealSerializer(meal).data, status=status.HTTP_201_CREATED)
