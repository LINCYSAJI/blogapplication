from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blog.models import Post,Profile

class SignUpForm(UserCreationForm):
    
    class Meta:
        
        model=User
        
        fields=["username","email","password1","password2"]
        
class SignInForm(forms.Form):
    
    username=forms.CharField()
    
    password=forms.CharField()

class BlogForm(forms.ModelForm):
    
    class Meta:
        model=Post
        exclude=("id","created_at","updated_at","author")
        
        widgets={
        
            "title":forms.TextInput(attrs={"class":"form-control"}),

            "slug":forms.TextInput(attrs={"class":"form-control"}),
        
            "Content":forms.Textarea(attrs={"class":"form-control"}),
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        
        model=Profile
        fields=["profile_picture","bio"]
    