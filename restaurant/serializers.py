from django.shortcuts import render
from rest_framework import serializers
from .models import *

class MealSerializer(serializers.ModelSerializer):
    #category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Meal
        fields = ['id', 'name', 'img_url', 'category', 'price', 'discount',]


   