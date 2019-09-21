from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import Http404

import json
from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import Meal, Restaurant, Order, Order_Detail

from rest_framework import generics

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from rest_framework_jwt.views import obtain_jwt_token 
from rest_framework_jwt.settings import api_settings

from .permissions import IsAdminOrReadOnly

#from posts.api.permissions import IsOwnerOrReadOnly
#from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response



User = get_user_model()

from rest_framework_jwt.settings import api_settings
from django.core.serializers import serialize

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    MealSerializer,
    RestaurantSerializer,
    OrderSerializer,
    MealOrderSerializer,
    )

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': 'mmm'
    }

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        #token, created = Token.objects.get_or_create(user=user)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # get retaurant
        restaurant = 0
        restaurantSerializer = "There is no restaurant data"
        mealSerializer = "There is no meals data"
        try:
            restaurant = Restaurant.objects.get(owner=user.pk)
            #restaurant = Restaurant.objects.all()
            restaurant_context = {
                "id":restaurant.id,
                "name":restaurant.name,
                "img_url":restaurant.img_url,
                "location":restaurant.location,
                "rest_type":restaurant.rest_type,
                "opening_hours":restaurant.opening_hours,
                "closing_hours":restaurant.closing_hours,
                "rating":restaurant.rating
            }
        except:
            pass 

        try:
            meals = Meal.objects.filter(restaurant=restaurant.pk)
            meal_context = []
            for meal in meals:
                meal_context.append( {
                    'name' : meal.name,
                    'img_url' : meal.img_url,
                    'category' : meal.category.name,
                    'price' : meal.price,
                    'discount' : meal.discount,
                    'restaurant' : meal.restaurant.id,
                    'rating' : meal.rating,
                    'delivery' : meal.delivery,
                    'delivery_fee' : meal.delivery_fee,
                    'quantity' : meal.quantity,
                    'available' : meal.available
                    } )
        except:
            pass
        
        #restaurant = Restaurant.objects.all()
        #restaurantSerializer = serializers.serialize('json',restaurant)
        user_context = {
            'user_id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return JsonResponse({
            'token': token,
            'user': user_context,
            'restaurant': restaurant_context,
            'meals': meal_context
        })

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]




class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(self.request.user)
            token = jwt_encode_handler(payload)
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PostListAPIView(ListAPIView):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        if self.request.user.is_authenticated():
            if(self.request.user.groups.filter(name="restaurant").exists()):
                restaurant = Restaurant.objects.get(owner=self.request.user.pk)
                queryset_list = Meal.objects.filter(restaurant=restaurant.id)
                return queryset_list
        else:
            queryset_list = Meal.objects.all() #filter(user=self.request.user)
            query = self.request.GET.get("q")
            if query:
                queryset_list = queryset_list.filter(restaurant=query)
            return queryset_list

class MealAPIView(ListAPIView):
    serializer_class = MealSerializer
    queryset = Meal.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = MealSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MealList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = MealSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class MealDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MealSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MealSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=HTTP_200_OK)



class RestaurantList(generics.ListCreateAPIView):
	permission_classes = [IsAdminOrReadOnly]
	queryset = Restaurant.objects.all()
	serializer_class = RestaurantSerializer




class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = Restaurant.objects.all()
	serializer_class = RestaurantSerializer


class OrderList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if(self.request.user.groups.filter(name="restaurant").exists()):
                restaurant = Restaurant.objects.get(pk=self.request.user.pk)
                queryset = Order.objects.filter(restaurant=restaurant)
                #snippets = Meal.objects.filter(restaurant=1)
            else:
                queryset = Order.objects.all()
        else:
            queryset = Order.objects.all()
        return queryset



class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = Order.objects.all()
	serializer_class = OrderSerializer

class OrderrList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    serializer_class = MealOrderSerializer

def add_restataurants(restaurants_objects, restaurant, meal):
    for i in range(len(restaurants_objects)):
        if(restaurants_objects[i]['restaurant'].id == restaurant.id):
            return i
    return True

@csrf_exempt
def setMealAvailability(request, pk):
    received_json_data=json.loads(request.body)
    try:
        available = received_json_data['available']
        if type(available) is not bool:
            return JsonResponse({
                            'message': "check spelling or data passed is not boolean"
                        }, safe=False, status=404)
    except:
        return JsonResponse({
                            'message': "check spelling or data passed is not boolean"
                        }, safe=False, status=404)
    try:
        meal = Meal.objects.get(id=pk)
        meal.available = available
        meal.save()
        return JsonResponse({
        'message': "update is done."
        }, safe=False)
    except Exception as e:
        return JsonResponse({
        'message': "meal is not in our records, check id"
        }, safe=False, status=404)
        

@csrf_exempt
def saveOrder(request):
    received_json_data=json.loads(request.body)
    
    personName = received_json_data['personName']
    personPhone = received_json_data['personPhone']
    personAddress = received_json_data['personAddress']
    restaurant = received_json_data['restaurant']
    meals = received_json_data['meal']
    order_quantity = received_json_data['order_quantity']
    status = received_json_data['status']
    note = received_json_data['note']

    ref_number = "old app no ref"
    try:
        ref_number = received_json_data['ref_number']
    except Exception as e:
        raise e
    
    restaurants = []
    orders = []
    meals_objects = []
    restaurants_objects = []
    restaurants_objects_context = []
    order_quantities = order_quantity.split(",")
    meal_ids = meals.split(",")

    for i in range(len(meal_ids)):
        meal = Meal.objects.get(pk=meal_ids[i])
        res = add_restataurants(restaurants_objects, meal.restaurant, meal)
        if(res):
            restaurants_objects.append({'restaurant':meal.restaurant, 'meal':[{'data':meal, 'quantity':order_quantities[i]}]})
        else:
            restaurants_objects[res]['meal'].append({'data':meal, 'quantity':order_quantities[i]})
    
    for restaurant_object in restaurants_objects:

        order = Order(restaurant=restaurant_object['restaurant'], status=status, name=personName, phone=personPhone, address=personAddress, note=note, ref_number=ref_number)
        order.save()
        for meal_obj in restaurant_object['meal']:
            meal_object=meal_obj['data']
            order_detail = Order_Detail.objects.create(name=meal_object.name,price=meal_object.price,discount=meal_object.discount,restaurant=meal_object.restaurant.id, status=status, quantity=meal_obj['quantity'])
            order_detail.save()
            order.order_detail.add(order_detail.id)

    

    #return JsonResponse({'message': "Your order has been placed thank you."})
    #return json.dumps({'message': "Your order has been placed thank you.", 'response':received_json_data})
    
    return JsonResponse({
        'message': "Your order has been placed thank you."
        }, safe=False)