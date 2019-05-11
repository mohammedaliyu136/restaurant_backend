from django.http import JsonResponse
from .models import Meal, Customer, Order, Restaurant
from .serializers import MealSerializer
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render, redirect


def index(request):
    queryset = Meal.objects.all()
    
    serializer = MealSerializer(queryset, many=True)
    return JsonResponse({'message': "not post", "meal":serializer.data})

@csrf_exempt
def order(request):
    if request.method=="POST":
        name       = request.POST['name']
        address    = request.POST['address']
        phone      = request.POST['phone']
        additional = request.POST['additional']
        meal_id    = json.loads(request.POST['meal_id'])

        customer = Customer.objects.create(name=name, address=address, phone_number=phone)
        customer.save()
        customer_id = customer.id

        rest = Restaurant.objects.get(id=1)

        order = Order.objects.create(customer=customer, restaurant=rest, status="ordered", additional_message=additional)
        #order.restaurant_id = rest,
        #order.customer_id = customer_id.id,
        order.save()

        for m_id in meal_id:
            if m_id != "":
                meal = Meal.objects.get(id=m_id)
                order.meal.add(meal)
        

    return JsonResponse({'message': "Thank you for your order. Can't wait to serve you again."})


def order_list(request):
    orders = Order.objects.all()
    print orders
    for order in orders:
        print order.customer.name, order.customer.address, order.customer.phone_number, order.meal.all()
        

    return render(request, 'order_list_index.html', {'orders':orders})