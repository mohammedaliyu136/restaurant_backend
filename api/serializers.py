from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model



from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )
from .models import Meal, Restaurant, Order, Order_Detail


User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]




class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data


    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value



    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                username = username,
                email = email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    #email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'username',
            #'email',
            'password',
            'token',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        username = data['username']
        password = data['password']
        user_qs = User.objects.filter(username=email)
        if user_qs.exists():
            user_qs[0]
            password

        return data


class MealSerializer(ModelSerializer):
    class Meta:
        model = Meal
        #fields = ('url', 'username', 'email', 'groups')
        fields = '__all__'


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        #fields = ('url', 'username', 'email', 'groups')
        fields = '__all__'

    def validate(self, data):
        return data



class OrderSerializer(ModelSerializer):
    meal = MealSerializer(many=True)
    class Meta:
        model = Order
        #fields = ('url', 'username', 'email', 'groups')
        fields = '__all__'
    
    def create(self, validated_data):
        meals_data = validated_data.pop('meal')
        order = Order.objects.create(**validated_data)
        for meal_id in meals_data:
            order.meal.add(Meal.objects.get(pk=meal_id))
        return order

    def validate(self, data):
        meal = Meal.objects.get(pk=meal_id)
        data['name'] = meal.name
        data['img_url'] = meal.img_url
        data['category'] = meal.category
        data['price'] = meal.price
        data['discount'] = meal.discount
        data['restaurant'] = meal.restaurant
        return data

class MealOrderDetailSerializer(ModelSerializer):
    class Meta:
        model = Order_Detail
        #fields = ('url', 'username', 'email', 'groups')
        fields = '__all__'


class MealOrderSerializer(ModelSerializer):
    order_detail = MealOrderDetailSerializer(many=True)
    class Meta:
        model = Order
        #fields = ('url', 'username', 'email', 'groups')
        fields = '__all__'