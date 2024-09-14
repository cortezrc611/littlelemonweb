from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Menu, Booking

class MenuAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu = Menu.objects.create(name="Burger", price=10.00, description="Tasty")

    def test_menu_list(self):
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.menu.name)

    def test_menu_detail(self):
        response = self.client.get(reverse('menu-detail', args=[self.menu.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.menu.name)

class BookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.booking = Booking.objects.create(name="John Doe", reservation_date=date.today(), reservation_time="12:00")

    def test_reservations_for_date(self):
        response = self.client.get(reverse('reservations_for_date') + '?date=' + str(date.today()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.booking.name)
