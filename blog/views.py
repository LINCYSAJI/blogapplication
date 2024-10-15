from django.shortcuts import render,redirect
from django.views.generic import View
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from  blog.models import Post,Profile
from blog.forms import BlogForm,SignUpForm,SignInForm,ProfileForm

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

from blog.decorators import Signin_required


class SignUpView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=SignUpForm()
        
        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=SignUpForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            print("account Created")
            
            return redirect("login")
        print("not created")
        return render(request,"register.html",{"form":form_instance})

class LoginView(View):
    
    def get(self,request,*args,**kwargs):
        
        form_instance=SignInForm()
        
        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        form_instance=SignInForm(request.POST)
        
        if form_instance.is_valid():
            
            data=form_instance.cleaned_data
            
            uname=data.get("username")
            
            pwd=data.get("password")
            
            user_object=authenticate(request,username=uname,password=pwd)
            
            print(user_object)
            
            
            if user_object:
                
                login(request,user_object)
                
                print("successfully login")
                
                return redirect("home")
            
        print("login failed")
        
        return render(request,"login.html",{"form":form_instance})
    




@method_decorator(Signin_required,name="dispatch")
class BlogCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=BlogForm()
        
        return render(request,'blog_create.html',{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        form_instance=BlogForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.instance.author=request.user
            
            form_instance.save()
            
            messages.success(request,"blog added sucessfully")
            
            return redirect("home")
        else:
            
            messages.error(request,"failed to add blog")
            
            return render(request,"blog_create.html",{"form":form_instance})
            
            
    
    
        

class BlogListView(View):
    
    def get(self,request,*args, **kwargs):
        form_instance=BlogForm()
        qs=Post.objects.all()
        return render(request,'home.html',{"form":form_instance,"data":qs})

class BlogDetailView(generic.DetailView):
    
    model = Post
    
    template_name = 'blog_details.html'
    
    
@method_decorator(Signin_required,name="dispatch")
class BlogDeleteView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        
        Post.objects.get(id=id).delete()
        
        return redirect("home")
    



@method_decorator(Signin_required,name="dispatch")
class BlogUpdateView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        blog_object=Post.objects.get(id=id)
        
        form_instance=BlogForm(instance=blog_object)
        
        return render(request,"blog_edit.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        blog_object=Post.objects.get(id=id)
        
        form_instance=BlogForm(instance=blog_object,data=request.POST)#update/ if form_instance contain instance then it perform update function
        
        if form_instance.is_valid():
            
            form_instance.save()

            messages.success(request,"blog changed")

            return redirect("home")
        else:
            messages.error(request,"failed to update")

            return render(request,"blog_edit.html",{"form":form_instance})
        
        
        
class DisplayProfileView(generic.DetailView):
    
    model=Profile
    
    template_name= 'user_detail.html'
    
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user
    
    
    
class SignOutView(View):
    
    def get(self,request,*args, **kwargs):
        
        logout(request)

        return redirect("login")
    
class ProfileUpdateView(LoginRequiredMixin, generic.TemplateView):
    profile_form=ProfileForm
    template_name="profile_edit.html"
    
    def post(self,request,*args, **kwargs):
        
        post_data=request.POST or None
        
        file_data=request.FILES or None
        
        profile_form=ProfileForm(post_data,file_data,instance=request.user)
        
        if profile_form.is_valid():
            
            profile_form.save()
            
            messages.success(request,"your profile was successfully updated")
            
            return redirect("user-profile")
        context=self.get_context_data(profile_form=profile_form)
        
        return self.render_to_response(context)
    def get(self,request,*args, **kwargs):
        
        return self.post(request,*args, **kwargs)
            