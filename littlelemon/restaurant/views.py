from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib import messages
from datetime import date, timedelta
from rest_framework import viewsets, generics
from .models import Menu, MenuItem, Category, Booking
from .forms import BookingForm
from .serializers import ReservationSerializer, MenuItemSerializer, CategorySerializer, MenuSerializer
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign-in')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class MenuListView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def booking(request):
    today = date.today()
    bookings = Booking.objects.filter(reservation_date=today)

    booked_times = [booking.reservation_time.strftime('%H') for booking in bookings]

    if request.method == 'POST':
        form = BookingForm(request.POST, booked_times=booked_times)
        if form.is_valid():
            reservation_date = form.cleaned_data.get('reservation_date')
            reservation_time = form.cleaned_data.get('reservation_time')

            if Booking.objects.filter(reservation_date=reservation_date, reservation_time=reservation_time).exists():
                form.add_error(None, 'This reservation slot is already booked.')
            else:
                form.save()
                messages.success(request, 'Your booking was successful!')
        else:
            messages.error(request, 'There was an error with your booking. Please try again.')
    else:
        form = BookingForm(booked_times=booked_times)

    return render(request, 'book.html', {
        'form': form,
        'current_date': today,
        'bookings': bookings,
        'booked_times': booked_times,
    })

@login_required
def menu(request):
    menu_items = Menu.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

@login_required
def display_menu_items(request, pk):
    menu_item = get_object_or_404(Menu, pk=pk)
    menu_items = Menu.objects.all().order_by('name')
    return render(request, 'menu_item.html', {
        'menu_item': menu_item,
        'menu_items': menu_items
    })

@login_required
def reservations_data(request):
    start_date = date.today()
    end_date = start_date + timedelta(days=7)

    bookings = Booking.objects.filter(reservation_date__range=[start_date, end_date])

    bookings_by_date = {}
    for booking in bookings:
        booking_date = booking.reservation_date.strftime('%Y-%m-%d')
        if booking_date not in bookings_by_date:
            bookings_by_date[booking_date] = []
        reservation_slot_number = int(booking.reservation_date.strftime('%Y%m%d')) * 10000 + int(booking.reservation_time.strftime('%H%M'))
        bookings_by_date[booking_date].append({
            'model': 'restaurant-booking',
            'pk': booking.pk,
            'name': booking.name,
            'reservation_time': booking.reservation_time.strftime('%H:%M'),
            'reservation_slot': reservation_slot_number,
        })

    return render(request, 'reservations.html', {
        'bookings_json': bookings_by_date
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def reservations_for_date(request):
    date = request.GET.get('date')

    if not date:
        return Response({"detail": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(reservation_date=date)
    serializer = ReservationSerializer(bookings, many=True)
    return Response(serializer.data)

class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date', None)
        if date:
            return Booking.objects.filter(reservation_date=date)
        return Booking.objects.none()


class CustomLogoutView(DjangoLogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # Ensure redirection to the login page
        return HttpResponseRedirect('/login/')
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Set cache-control headers to prevent caching
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response