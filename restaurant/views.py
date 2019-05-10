from django.http import JsonResponse
from .models import Meal
from .serializers import MealSerializer


def index(request):
    queryset = Meal.objects.all()
    
    serializer = MealSerializer(queryset, many=True)
    return JsonResponse({'message': "not post", "meal":serializer.data})