from django import forms
from .models import Booking
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
# Code added for loading form data on the Booking page




class BookingForm(forms.ModelForm):
    # List of hours for the dropdown in 12-hour format
    HOURS = [(f"{i:02}:00", f"{i % 12 or 12}:00 {'AM' if i < 12 else 'PM'}") for i in range(24)]

    reservation_time = forms.ChoiceField(
        choices=HOURS,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'reservation_time'})  # Add id for JavaScript
    )

    class Meta:
        model = Booking
        fields = ['name', 'reservation_date', 'reservation_time']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        booked_times = kwargs.pop('booked_times', [])
        super().__init__(*args, **kwargs)

        # Set the current date as the initial value for reservation_date
        self.fields['reservation_date'].initial = timezone.now().date()

        # Convert booked times to 12-hour format for comparison
        booked_times_12hr = [f"{int(time):02}:00 {'AM' if int(time) < 12 else 'PM'}" for time in booked_times]

        # Remove booked time slots from the dropdown choices
        available_choices = [(value, label) for value, label in self.HOURS if value not in booked_times_12hr]
        self.fields['reservation_time'].choices = available_choices