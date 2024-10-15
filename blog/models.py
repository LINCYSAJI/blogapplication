from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.



    

class Post(models.Model):
    
    title=models.CharField(max_length=200,unique=True)
    
    author=models.ForeignKey(User,on_delete=models.CASCADE)
        
    content=models.TextField()
    
    created_at=models.DateTimeField(auto_now_add=True)
    
    updated_at=models.DateTimeField(auto_now=True)
    
    slug=models.SlugField(max_length=1000,null=True,blank=True)
    
    class Meta:
        
        ordering=['-created_at']
        
    def __str__(self):
        return self.title
    

class Profile(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.TextField(max_length=500,blank=True)
    
    profile_picture=models.ImageField(upload_to='profile_images', null=True, blank=True, default='profile_images/default.jpg')
    
    def __str__(self):
        return self.user.username