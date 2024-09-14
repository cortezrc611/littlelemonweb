from django.urls import path
from . import views  # Import all views from the current app's views.py
from .views import MenuListView, MenuDetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .views import signup_view, login_view
from .views import CustomLogoutView
from .views import CategoriesView
restaurant = 'api'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.booking, name='book'),  # Ensure this matches the view name
    path('menu/', views.menu, name='menu'),  # Ensure this matches the view name
    path('menu_item/<int:pk>/', views.display_menu_items, name='menu_item'),  # Ensure this matches the view name
    path('reservations/', views.reservations_data, name='reservations_data'),
    path('bookings/', views.reservations_for_date, name='reservations_for_date'),
    path('api/categories/', CategoriesView.as_view(), name='api-categories'),
    path('menu-items/', views.MenuItemListView.as_view(), name='menu-item-list'),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-item-detail'),
    path('api/menu-items/', MenuListView.as_view(), name='menu-list'),
    path('api/menu-items/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
     path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='sign-in'),
      path('logout/', CustomLogoutView.as_view(), name='logout'),
    
]

