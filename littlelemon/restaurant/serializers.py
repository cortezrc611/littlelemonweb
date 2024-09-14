from rest_framework import serializers
from .models import Booking
from .models import MenuItem, Category
from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'price', 'description']

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory','category','category_id']

class ReservationSerializer(serializers.ModelSerializer):
    model = serializers.SerializerMethodField()
    pk = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = ['model', 'pk', 'name', 'reservation_date', 'reservation_time', 'reservation_slot']

    def get_model(self, obj):
        return 'restaurant-booking'

class BookingSerializer(serializers.Serializer):
    model = serializers.CharField()
    pk = serializers.IntegerField()
    name = serializers.CharField()
    reservation_time = serializers.CharField()
    reservation_slot = serializers.IntegerField()