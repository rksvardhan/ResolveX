from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from django.shortcuts import render, redirect
from .models import Profile,Complaint
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import requests

class ComplaintForm(forms.ModelForm):
    Subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter complaint subject...',
            'required': True
        })
    )
    Type_of_complaint = forms.ChoiceField(
        choices=[
            ('ClassRoom', 'ClassRoom'),
            ('Teacher', 'Teacher'),
            ('Management', 'Management'),
            ('College', 'College'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    Description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Please provide a detailed description of your complaint...',
            'required': True
        })
    )
    
    class Meta:
        model = Complaint
        exclude = ['user', 'priority', 'status', 'Time', 'ai_analysis']

class UserProfileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('collegename','contactnumber','Branch')
    

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
    def clean_email(self):
            # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

'''class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location',)'''
    
class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username...',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'Enter email...'
        })
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name...',
            'required': True
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name...',
            'required': True
        })
    )
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
    
    def clean_email(self):
            # Get the email
        username = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.exclude(pk=self.instance.pk).get(username=username)
            
            
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return username

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


class UserProfileUpdateform(forms.ModelForm):
    
    collegename = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'College name...'
        })
    )
    contactnumber = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact number...',
            'required': True
        })
    )
    Branch = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'Branch...'
        })
    )
    type_user = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('grievance', 'Grievance Member')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )

    class Meta:
        model=Profile
        fields=('collegename','contactnumber','Branch','type_user')

class statusupdate(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=('status',)  
        help_texts = {
            'status': None,
          
        }      
